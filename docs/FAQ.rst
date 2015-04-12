FAQ
===

MonkeyPatching is bad. Why do you use it?
-----------------------------------------

Yes MonkeyPatching is bad and if I had control over everything I would gladly extends or subclass whatever is being monley-patched by Polla. Unfortunately I don't.

Everything which is being monkey-patched by POLLA can be achieved in other ways by creating a replacement for ``django.contrib.sites`` which would be extending the existing code-base. And it would be a **much better practice**.
But doing so would **break compatibility** with any third party library whcih already uses ``django.contrib.sites``.

If you find a way around that, feel free to contribute.