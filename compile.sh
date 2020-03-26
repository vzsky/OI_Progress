cd app
zip -r ../app.zip *
cd ..
echo '#!/usr/bin/env python3' | cat - app.zip > oiprog
chmod +x oiprog
rm app.zip