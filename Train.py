# train.py
import os
import sqlite3
import datetime
import pickle
import configargparse
from pyannote.audio import PretrainedSpeakerEmbedding
from diarize import chunk_audio  # your existing chunking logic

def init_db(db_path):
    conn = sqlite3.connect(db_path)
    conn.execute("""
      CREATE TABLE IF NOT EXISTS speakers (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL UNIQUE
      )
    """)
    conn.execute("""
      CREATE TABLE IF NOT EXISTS embeddings (
        id INTEGER PRIMARY KEY,
        speaker_id INTEGER NOT NULL,
        vector BLOB NOT NULL,
        timestamp DATETIME NOT NULL,
        FOREIGN KEY(speaker_id) REFERENCES speakers(id)
      )
    """)
    conn.commit()
    return conn

def upsert_speaker(conn, name):
    cur = conn.cursor()
    cur.execute("INSERT OR IGNORE INTO speakers(name) VALUES(?)", (name,))
    conn.commit()
    cur.execute("SELECT id FROM speakers WHERE name = ?", (name,))
    return cur.fetchone()[0]

def insert_embedding(conn, speaker_id, vector):
    blob = pickle.dumps(vector)
    ts = datetime.datetime.utcnow().isoformat()
    conn.execute(
      "INSERT INTO embeddings(speaker_id, vector, timestamp) VALUES(?,?,?)",
      (speaker_id, blob, ts)
    )
    conn.commit()

def train(args):
    if not args.speaker:
        raise ValueError("At least one --speaker NAME PATH pair is required")
    model = PretrainedSpeakerEmbedding(
      args.embedding_model, device=args.device
    )
    conn = init_db(args.db_path)
    for name, path in args.speaker:
        if not os.path.isfile(path):
            raise FileNotFoundError(f"{path} not found")
        speaker_id = upsert_speaker(conn, name)
        segments = chunk_audio(path, duration=args.chunk_duration)
        for segment in segments:
            emb = model({'audio': path, 'segment': segment})
            insert_embedding(conn, speaker_id, emb.numpy())
    conn.close()

def main():
    p = configargparse.ArgParser(
      description="Transcribbler speaker-training subcommand"
    )
    sub = p.add_subparsers(dest="command", required=True)
    tr = sub.add_parser("train")
    tr.add_argument(
      "--speaker", nargs=2, action="append",
      metavar=("NAME","PATH"),
      help="Labelled WAV file for one speaker"
    )
    tr.add_argument(
      "--db-path", default="transcribbler.db",
      help="SQLite database path"
    )
    tr.add_argument(
      "--chunk-duration", type=float, default=3.0,
      help="Chunk length in seconds"
    )
    tr.add_argument(
      "--embedding-model", default="speechbrain/spkrec-ecapa-voxceleb",
      help="Hugging Face model for speaker embeddings"
    )
    tr.add_argument("--device", default="cpu", help="torch device")
    args = p.parse_args()
    if args.command == "train":
        train(args)

if __name__ == "__main__":
    main()


# tests/test_train.py
import os
import sqlite3
import subprocess
import tempfile
import numpy as np
import wave
import contextlib
import pytest

def make_sine_wav(path, freq=440, duration=1.0, rate=16000):
    samples = (np.sin(2*np.pi*np.arange(rate*duration)*freq/rate)*32767).astype(np.int16)
    with wave.open(path, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(rate)
        wf.writeframes(samples.tobytes())

@pytest.fixture
def two_speakers(tmp_path):
    a = tmp_path / "alice.wav"
    b = tmp_path / "bob.wav"
    make_sine_wav(str(a), freq=440)
    make_sine_wav(str(b), freq=550)
    db = tmp_path / "test.db"
    return str(a), str(b), str(db)

def test_train_end_to_end(two_speakers):
    alice_wav, bob_wav, db_path = two_speakers
    cmd = [
      "python", "train.py", "train",
      "--speaker", "Alice", alice_wav,
      "--speaker", "Bob",   bob_wav,
      "--db-path", db_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT name FROM speakers ORDER BY name")
    names = [row[0] for row in cur.fetchall()]
    assert names == ["Alice", "Bob"]

    cur.execute("SELECT speaker_id, vector FROM embeddings")
    rows = cur.fetchall()
    ids = set(r[0] for r in rows)
    assert len(ids) == 2, "Expected one embedding per speaker chunk"
    for _, blob in rows:
        vec = pickle.loads(blob)
        assert isinstance(vec, np.ndarray)
        assert vec.ndim == 1
    conn.close()