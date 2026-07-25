import inspect

import app.main as main


print("=" * 50)
print("RUNTIME SCHEMA AUDIT")
print("=" * 50)


print("render_page source:")
source = inspect.getsource(main.render_page)

print(source[:2000])


print("\nlandingpage source:")
source2 = inspect.getsource(main.landingpage)

for line in source2.splitlines():

    if "schema" in line or "product_schema" in line:
        print(line)
