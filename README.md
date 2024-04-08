# Carbon page

Directory/file template tool to reuse structures easily.

## Usage

Suppose you have a project with repetitive structures (like a Web App),
and you have a pre-defined structure for modules.

```
your-project/
    src/
        module/
            __init__.py
            module_controller.py
            module_repository.py
            module_schema.py
        module2/
            __init__.py
            module2_controller.py
            module2_repository.py
            module2_schema.py
...
```
You might want to reproduce the same structure when creating a new module sticking to the "convention" you've already stablished in your project.

It could be as simple as copying some existing module and change its content. But as soon as the modules grow, you might have to refactor lots of files before you can even start coding.

### Templates folder
You could reuse existing structures that are not attached to a particular content and can be customized with variables. Something like this:
```
your_project/
    src/
    templates/
        modules
            {{ module }}/
                __init__.py
                {{ module }}_controller.py
                {{ module }}_repository.py
                {{ module }}_schema.py
```

Then you run the following command
```shell
python -m carbonpage dir templates/module "src/{{ module }}" -c module:users
```
After that your project will have a new module like this:
```
your_project/
    src/
        ...
        users/
            __init__.py
            users_controller.py
            users_repository.py
            users_schema.py
        ...
    ...
```
You have saved the time to refactor an existing module and only care about coding some awesome feature in your app.

## Configuration
If your structure its not deeply nested, then the above command should do. But what happends when you have deeply nested structures? It might be a painful to remember all the path or even have to copy it in a separate file.

To get over this, you could use a proj.config.json file at the root of your project containing some reusable paths and data to simplify the command.
```json
{
    // Context are variables stored for reusing
    "context": {
        "a_variable": "a value" // This value will be accessible when usign the template
    },
    "template_dir": "root path for templates (optional)",
    "output_dir": "root path to store the created structure (optional)",
    "alias": {
        "example": {
            "template_dir": "example", // Where is the template structure 
            "output_dir": "output", // Where to store the output structure
            "context": "key1:value1,key2:value2", // Key value pairs to provide extra localized context (or a path of a json file).
            "dir": false // If the context variable refers to a path that should be read to retrieve context variables
        }
    }
}
```
- `context`: refers to variables to pass to the template system (Jinja).
- `template_dir`: predefined template path for all operations.
- `output_dir`: predefined output path for all operations, it can have variables. Example: `"output_dir": "{{ project_name }}"/src/{{ other_var }}`.
- `alias`: commands to set reusable command configurations.

### Example
Considering the following structure:
```
templates/
    package/
        __init__.py
        {{ package }}_config.py
    module/
        __init__.py
        {{ module }}.py
src/
    ...
```
And the following configuration file:
```json
{
    "templates_dir": "templates",
    "output_dir": "src",
    "alias": {
        "module": {
            "template_dir": "module", 
            "output_dir": "{{ module }}"
        }
    }
}
```
You could run 
```shell
python -m lunnaris-templates dir package "{{ package }}" -c package:auth
```
Then your `src` directory would look like this:
```
src/
    ...
    auth/
        __init__.py
        auth_config.py
```
You could also use the alias `module` to generate a folder for an specific module. 

Runing
```shell
python -m carbonpage alias module -c module:auth
```
your `src` folder will look like this:
```
src/
    ...
    auth/
        __init__.py
        auth.py
```
Carbonpage will look for the configuration file in the current working directory with the name `proj.config.json`. You could specify a different file using `-cf your_file.json` or `--config your_file.json`.

## Context
A context is a set of variables that can be passed to be used in the generation of the files. It's json representated. 

In the command line you could pass context in the form of `key:value` pairs separated by `,` with the option `-c` or `--context`.

Example
```shell
python -m carbon page ... -c "key1:value1,key2:value2"
```
Internally, this will be converted to
```
{
    "key1": "value1",
    "key2": "value2"
}
```
In line context only supports string values. If you need to pass a more complex context, you can pass the context as a path to a file using the flag `-d` or `--dir`.

Example
```shell
python -m carbonpage ... -d -c "my_context.json"
```
The `my_context.json` file
```json
{
    "key1":"value1",
    "key2":{
        "subkey1": "value"
    }
}
```
Complex context is usually used to populate the content of the files using `Jinja`. 

Suppose you have a template file that contains the following:
```
# Created by: {{ author.name }}
# Contact: {{ author.email }}
```
You would need a context that looks like this
```json
{
    "author": {
        "name": "John Doe",
        "email": "john.doe@example.com"
    }
}
```




