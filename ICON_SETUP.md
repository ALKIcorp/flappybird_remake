# Setting Up App Icon

To add a custom icon to your Flappy Bird app:

1. **Create an .icns file:**
   - Option A: Use `iconutil` (macOS built-in)
     ```bash
     # Create an iconset directory
     mkdir icon.iconset
     
     # Copy your icon images (PNG) with specific sizes:
     # icon_16x16.png, icon_16x16@2x.png (32x32)
     # icon_32x32.png, icon_32x32@2x.png (64x64)
     # icon_128x128.png, icon_128x128@2x.png (256x256)
     # icon_256x256.png, icon_256x256@2x.png (512x512)
     # icon_512x512.png, icon_512x512@2x.png (1024x1024)
     
     # Convert to .icns
     iconutil -c icns icon.iconset
     ```
   
   - Option B: Use online converter or Image2icon app

2. **Update flappybird.spec:**
   - Change `icon=None` to `icon='path/to/your/icon.icns'`

3. **Rebuild:**
   ```bash
   ./build_app.sh
   ```

