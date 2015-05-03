import json
import zipfile

from xml.dom import minidom

import jinja2
from paver.easy import *

class FileReader(dict):
    def __call__(self, *args, **kwargs):
        return self.__getitem__(*args, **kwargs)

    def __missing__(self, filepath):
        text = path(filepath).text(encoding='utf-8')
        self[filepath] = text
        return text

def render_template(template_path, context):
    global template_env

    template = template_env.get_template(template_path)
    return template.render(context)

def package_files(output, files):
    with zipfile.ZipFile(output, 'w') as z:
        for f in files:
            z.write(f['src'], f['dest'])

def xml_cdata(data):
    cdata = minidom.CDATASection()
    cdata.data = data
    return cdata.toxml()

file_reader = FileReader()

spec = None
spec_file = path.getcwd()/"workflow.json"

build_dir = path.getcwd()/"build"
template_output = build_dir/"info.plist"

templates_dir = path.getcwd()/"templates"
template_loader = jinja2.FileSystemLoader(templates_dir.abspath())
template_env = jinja2.Environment(loader=template_loader)

template_env.globals['files'] = file_reader
template_env.filters['cdata'] = xml_cdata

@task
@no_help
def load_spec():
    global spec, spec_file, file_reader

    if spec is None:
        spec = json.loads(file_reader(spec_file))

@task
@no_help
def create_build_dir():
    global build_dir

    build_dir.makedirs()

@task
@needs(['create_build_dir', 'load_spec'])
def template():
    global spec, template_output

    rendered_text = render_template("info.plist.j2", spec)
    template_output.write_text(rendered_text, encoding='utf-8')

@task
@needs(['template'])
def build():
    pass

@task
@needs(['load_spec', 'build'])
def package():
    global spec, build_dir, template_output

    filename = "%s.alfredworkflow" % (spec['id'].split('.')[-1])
    workflow_output = build_dir/filename
    files = [{'src': path(src).abspath(), 'dest': dest} for dest, src in spec['icons'].iteritems()]
    files.insert(0, {'src': template_output, 'dest': 'info.plist'})
    package_files(workflow_output, files)

    print("Workflow created in %s" % (workflow_output.relpath()))
