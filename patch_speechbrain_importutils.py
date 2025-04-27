# hooks/patch_speechbrain_importutils.py

try:
    import speechbrain.utils.importutils as importutils
    # Replace the bits that do filesystem scans with no‑ops
    importutils.lazy_export_all = lambda *args, **kwargs: None
    importutils.find_imports    = lambda *args, **kwargs: []
except ImportError:
    # if speechbrain isn’t present yet, ignore
    pass