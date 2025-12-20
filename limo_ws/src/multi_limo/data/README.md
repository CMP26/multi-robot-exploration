# Target Image Directory

Place your target object image here.

**Requirements:**

- Format: PNG or JPG
- RGB color image
- Should contain sufficient texture for ORB feature extraction
- Recommended size: 640x480 or larger

**Example:**

- `target_object.png` - Main target object to detect

**Usage:**
Set the `target_image_path` parameter in the launch file to point to your image:

```xml
<param name="target_image_path" value="$(find multi_limo)/data/target_object.png"/>
```
