import os
import click, colorama
import json
from .templates import TemplateGenerator

accent = colorama.Fore.CYAN
reset = colorama.Style.RESET_ALL
default_config = "carbonpage.config.json"

def transform_string(data: str):
    data = data.strip()
    if "," in data:
        return data.split(",")
    return data

def transform_context(context: str) -> dict:
    transformed_context = {}
    for key_value in context.split(","):
        split_key_value = key_value.split(":")
        if len(split_key_value) != 2:
            continue
        key, value = key_value.split(":")
        transformed_context[key] = transform_string(value)
    return transformed_context

def load_config(template_dir: str, output_dir: str, context: str="", dir: bool=False, config: dict={}):
    if dir:
        context = json.load(open(context))
    else:
        context = transform_context(context)

    if "context" in config:
        config["context"].update(context)
        context = config["context"]

    if "templates_dir" in config:
        template_dir = os.path.join(config["templates_dir"], template_dir)
        template_dir = template_dir.replace("\\", "/")

    if "output_dir" in config:
        output_dir = os.path.join(config["output_dir"], output_dir)
        output_dir = output_dir.replace("\\", "/")
    
    return {
        "context": context,
        "template_dir": template_dir,
        "output_dir": output_dir,
    }

@click.group()
def commands():
    pass

@click.command("dir", help="Generate a template from a directory")
@click.argument("template_dir")
@click.argument("output_dir")
@click.option(
    "--context", "-c", default="",
    help="Context for the command (key1:value1;key2:value2) or /path (using -d|--dir).")
@click.option("--dir","-d", is_flag=True, help="Use the context from a file")
@click.option("--config", "-cf", help=f"Path to the configuration file (default: {default_config})", 
              default=f"{default_config}")

def generate_from_dir(template_dir: str, output_dir: str, context: str="", dir: bool=False, config: str=default_config):
    config = json.load(open(config))
    template_root = config["templates_dir"] if "templates_dir" in config else ""
    config = load_config(template_dir, output_dir, context, dir, config)
    #template_dir = config["template_dir"]
    output_dir = config["output_dir"]
    context = config["context"]
    
    generator = TemplateGenerator(template_root)
    click.echo(f"Generating from {accent}{template_dir}{reset} to {accent}{output_dir}{reset}")
    generator.create(template_dir, output_dir, context)
    click.echo(f"Directory {accent}{template_dir}{reset} generated successfully!")

@click.command("alias", help="Generate a template from an alias")
@click.argument("alias")
@click.option(
    "--context", "-c", default="",
    help="Context for the command (key1:value1;key2:value2) or /path (using -d|--dir).")
@click.option("--dir","-d", is_flag=True, help="Use the context from a file")
@click.option("--config", "-cf", help=f"Path to the configuration file (default: {default_config})", 
              default=f"{default_config}")
def generate_from_alias(alias: str, context: str="", dir: bool=False, config: str=default_config):
    config = json.load(open(config))
    if alias not in config["alias"]:
        click.echo(f"Alias {accent}{alias}{reset} not found")
        return
    template_root = config["templates_dir"] if "templates_dir" in config else ""
    alias_data = config["alias"][alias]
    context = context if "context" not in alias_data else alias_data["context"]
    dir = dir if "dir" not in alias_data else alias_data["dir"]
    config = load_config(alias_data["template_dir"], alias_data["output_dir"], context, dir, config)
    template_dir = alias_data["template_dir"]
    output_dir = config["output_dir"]
    print(output_dir)
    context = config["context"]
    generator = TemplateGenerator(template_root)
    click.echo(f"Generating from alias {accent}{alias}{reset}")
    generator.create(template_dir, output_dir, context)
    click.echo(f"Alias {accent}{alias}{reset} executed successfully!")

@click.command(help="Create a configuration file example")
def config_example():
    click.echo(f"Creating config template example: {accent}{default_config}{reset}")
    with open(default_config, "w") as f:
        f.write(json.dumps({
            "templates_dir": "templates",
            "output_dir": "output",
            "context": {
                "a_variable": "a_value"
            },
            "alias": {
                "example": {
                    "template_dir": "example",
                    "output_dir": "output",
                    "context": "key1:value1,key2:value2",
                    "dir": False
                }
            }
        }, indent=4))
    
commands.add_command(generate_from_dir)
commands.add_command(generate_from_alias)
commands.add_command(config_example)

def run():
    colorama.init()
    commands()
