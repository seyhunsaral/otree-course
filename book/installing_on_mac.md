# Installing oTree on a Mac
I am not really the right person to talk about installing `oTree` on a Macintosh computer (see). However during my course, few people came to me with their problems with `oTree` installation and I was able to solve most of them with similar ways. 

* The first problem is when you install `pip install -U otree` you get an error message on gcc. It tells you something like:
```
error: command 'gcc' failed with exit status 1
```

  * Solution: 

`xcode-select --install`
`sudo xcodebuild -license`
