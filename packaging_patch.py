# Patch for packaging.version module
import sys

def patch_packaging_version():
    try:
        import packaging.version
        
        # Save the original parse function
        original_parse = packaging.version.parse
        
        # Create a patched version that handles empty strings
        def patched_parse(version):
            if version == '':
                return packaging.version.Version('0.0.0')  # Default version if empty
            return original_parse(version)
        
        # Replace the original with our patched version
        packaging.version.parse = patched_parse
        
        # Save the original InvalidVersion class
        original_invalid_version = packaging.version.InvalidVersion
        
        # Create a patched version that handles empty strings
        class PatchedInvalidVersion(original_invalid_version):
            def __init__(self, version):
                if version == '':
                    version = '0.0.0'  # Default version if empty
                super().__init__(version)
        
        # Replace the original with our patched version
        packaging.version.InvalidVersion = PatchedInvalidVersion
        
        # Also patch the Version class to handle empty strings
        original_version = packaging.version.Version
        
        class PatchedVersion(original_version):
            def __init__(self, version):
                if version == '':
                    version = '0.0.0'  # Default version if empty
                super().__init__(version)
        
        packaging.version.Version = PatchedVersion
        
        print("Patched packaging.version to handle empty version strings")
    except Exception as e:
        print(f"Error patching packaging.version: {e}")

# Apply the patch
patch_packaging_version()

# Also patch torch's version comparison which uses packaging
try:
    import torch.utils.imports
    if hasattr(torch.utils.imports, '_compare_version'):
        original_compare_version = torch.utils.imports._compare_version
        
        def patched_compare_version(version, target):
            if version == '':
                version = '0.0.0'
            if target == '':
                target = '0.0.0'
            return original_compare_version(version, target)
        
        torch.utils.imports._compare_version = patched_compare_version
        print("Patched torch.utils.imports._compare_version")
except Exception as e:
    print(f"Error patching torch.utils.imports: {e}")