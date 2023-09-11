import glob, os

for x in sorted(glob.glob("slides/*.pdf")):
    print(x)
    os.system(f"pdftoppm {x} {x} -png")
