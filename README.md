# dboard

`dboard` is a terminal dashboard, using python's [textualize/rich](https://github.com/textualize/rich) library and inspired by [wtfutil/wtf](https://github.com/wtfutil/wtf).

Allows to execute multiple commands, configured with a simple YAML file, and display the data output.
Provides a way to visualize, monitor and alert stats, systems changes, services status.

![](docs/img/example.gif)

### Features

* [x] execute multiple commands asynchronous
* [x] configure with a YAML file


### Development

Run locally:

```yml
# make help
Usage:
  env            :  create venv and install dependencies locally
  app            :  run app locally
  req            :  update requirements.txt
  bin            :  create binary file
  lint           :  lint code
  help           :  show help message
```


##### Dashboard alternatives:

* [wtfutil/wtf](https://github.com/wtfutil/wtf)
* [sqshq/sampler](https://github.com/sqshq/sampler)
* [mum4k/termdash](https://github.com/mum4k/termdash)
* [fdehau/tui-rs](https://github.com/fdehau/tui-rs)
* [yaronn/blessed-contrib](https://github.com/yaronn/blessed-contrib)
