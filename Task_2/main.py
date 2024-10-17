import zipfile
import re
import requests
from argparse import ArgumentParser


def download_package(url, package_path):
    response = requests.get(url)

    if response.status_code == 200:
        with open(package_path, 'wb') as f:
            f.write(response.content)
        print(f"Выполнена загрузка в {package_path}...")


def find_nuspec(nupkg_path):
    with zipfile.ZipFile(nupkg_path, 'r') as zf:
        # Ищем файл .nuspec, содержащий манифест
        for file in zf.namelist():
            if file.endswith('.nuspec'):
                with zf.open(file) as f:
                    return get_dependencies(f.read())
    return {}


def get_dependencies(data):

    nuspec_text = data.decode('utf-8')

    pattern_name = r'<id>([^<]+)'
    pattern_id = r'<dependency id="([^"]+)"'
    pattern_version = r'version="([^"]+)"'

    name = re.findall(pattern_name, nuspec_text)[0]
    dependencies_id = re.findall(pattern_id, nuspec_text)
    dependencies_version = re.findall(pattern_version, nuspec_text)

    dependencies = [name]
    for i in range(0, len(dependencies_id)):
        dependencies.append( dependencies_id[i] + " " + dependencies_version[i] )

    return dependencies

def build_graph(dependencies):
    graph = 'graph TD\n'
    name = dependencies[0]
    for i in range(1,len(dependencies)):
        graph += f'\tA([{name}]) --> B{i}([{dependencies[i]}])\n'
    return graph

def save_result(name_file, graph):
    graph = '```\n' + graph + '\n```'
    with open(name_file, 'w', encoding='utf-8') as f:
        f.write(graph)
    print(f"Код для описания графа зависимостей сохранен в: {name_file}...")

def visualize_graph(visualizer_path, graph_code):
    with open(visualizer_path, 'w', encoding='utf-8') as f:
        f.write(graph_code)
    print(f"Визуализация графа зависимостей сохранена в: {visualizer_path}...")

def main():
    parser = ArgumentParser(description="Visualization of the dependency graph")
    parser.add_argument("visualizer_path", help="Path to visualizer program")
    parser.add_argument("nupkg_path", help="Path to the .nupkg package")
    parser.add_argument("result_path", help="Path to the result file")
    parser.add_argument("repository_url", help="URL of the package repository")

    args = parser.parse_args()

    download_package(args.repository_url, args.nupkg_path)

    dependencies = find_nuspec(args.nupkg_path)

    # Create graph
    graph = build_graph(dependencies)

    save_result(args.result_path, graph)

    visualize_graph(args.visualizer_path, graph)

if __name__ == "__main__":
    main()
    # https://www.nuget.org/api/v2/package/Microsoft.Identity.Client/4.65.3-preview
    # https://www.nuget.org/api/v2/package/System.Diagnostics.EventLog/9.0.0-rc.2.24473.5
