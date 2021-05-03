oTree Architecture
============================

## What is oTree?

* oTree is a platform/software package to run online/lab experiments.

* Participants interact with the experimenters and with each other by using their browsers

* oTree runs on/as webserver 
    * It may run on your computer for development (local installation)
    * It runs on a physical server (Server setup)
    * It runs on cloud services (Heroku, oTree hub, AWS, DigitalOcean etc.)

* It has two modes:
   * Manual programming (Dominantly Python)
   * Point-and-click interface (oTree Studio)
   
* In this book, we teach and refer to the first mode.

* Point-and-click interface is available here: [oTree Studio](https://otree.readthedocs.io/en/latest/studio.html) (Free for small/medium-sized projects, paid subsription of the rest) 


(otree_architecture:comp)=
## oTree and z-Tree comparision
This comparison is for those who already use z-Tree {cite}`fischbacher2007z`. If you don't know what z-Tree is or have never used it, please feel free to skip it.

### `z-Tree` is click & run, `oTree` needs a server

```{figure} ../figures/otree_architecture_comp_ztree_1.png
---
---
z-Tree: Click and Run
```
```{figure} ../figures/otree_architecture_comp_otree_1.png
---

---
oTree: Server
```

If you use z-Tree, you know that, for a basic setup, all you need to do is to run `ztree.exe` on your server machine and `zleaf.exe` on your clients with few clicks and that's it. oTree is a little complicated than that. It should be running on a server.
   
   
### `z-Tree` needs client software, `oTree` doesn't.
  * With `z-Tree`, clients require software to run on their computer. With `oTree` they connect to the experiment with a web browser (Firefox, Chromium, Google Chrome, etc.).



```{bibliography} ../refs.bib
:filter: docname in docnames
:style: unsrt
```
