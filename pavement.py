import json
import zipfile

from paver.easy import *

workflow_spec = None
files = dict(
    spec="workflow.json",
    plist="info.plist",
)

def read_workflow_spec():
    if workflow_spec is None:
        with open(files['spec']) as f:
            return json.loads(f.read())

    return workflow_spec

@task
def package():
    spec = read_workflow_spec()
    filename = "%s.alfredworkflow" % (spec['id'].split('.')[-1])
    with zipfile.ZipFile(filename, 'w') as z:
        z.write(files['plist'], "info.plist")
        for icon_name, icon_file in spec['icons'].iteritems():
            z.write(icon_file, icon_name)
    print("Workflow created in %s" % (filename))
