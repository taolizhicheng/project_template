## 使用方法

根据项目路径生成项目模板
```shell
project-template \ 
--add \ 
--name <template-name> \ 
--project-dir <project-dir> \ 
--template-dir <save-dir> # optional, path to save template
```

根据项目路径更新项目模板
```shell
project-template \
--update \ 
--name <template-name> \ 
--project-dir <project-dir> \ 
--template-dir <save-dir>  # optional, path to save template
```

删除项目模板
```shell
project-template \ 
--delete \ 
--name <template-name>
```

查看项目模板
```shell
project-template \ 
--list \ 
--name <template-name>  # optional, list all templates if not specified
```

根据项目模板生成项目
```shell
project-template \ 
--instantiate \ 
--name <template-name> \ 
--project-dir <project-dir>
```