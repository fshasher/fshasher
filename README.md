## fshasher

Hash file objects across platforms.

Hash files is easy and usually built into the shell of a platform. This is important to know that the file has the contents it is supposed to or believed to have. However, for folders there is usually no easy provided solution since the computed hash depends on the definition. *fshasher* provides easy to use functionality so that folders can be hashed just like files and the results compared no matter the platform.

### Background

This library is intended for limited use right now. I came across this problem in multiple different other projects and rather than duplicating the code, went through the exercise of creating a library. There are handful of existing and similar libraries, namely [checksumdir](https://github.com/cakepietoast/checksumdir) and [dirhash](https://github.com/andhus/dirhash-python) but they haven't been updated for a few years and they make some decisions which I would prefer to do differently. Namely checksumdir does not take into account directory structure properly. It removes separators so that a AB/C/D.txt and AB/CD.txt would hash the same (assuming D.txt and CD.txt have the same contents). It also does not have the option to account for empty directories.

Neither library has been updated since 2020, and given the several python releases since then, it is clear that they are not tested against the latest versions or maintained to follow the latest best practices, even if the core logic would not be rendered incorrect.

### Installation

Like most python packages nowadays, fshasher can be installed on pip.

```
pip install fshasher
```
