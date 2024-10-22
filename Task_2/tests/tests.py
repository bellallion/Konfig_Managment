import unittest
from unittest.mock import patch, mock_open
import Task_2.main as m
import zipfile
import tempfile
import os

class TestDependencyGraph(unittest.TestCase):

    @patch('requests.get')
    def test_download_package_success(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.content = b'Test content'

        with patch('builtins.open', mock_open()) as mocked_file:
            m.download_package('https://www.nuget.org/api/v2/package/System.Diagnostics.EventLog/9.0.0-rc.2.24473.5', 'test.nupkg')
            mocked_file.assert_called_once_with('test.nupkg', 'wb')

    def test_find_nuspec(self):
        with tempfile.NamedTemporaryFile(delete=False, suffix='.nupkg') as temp_nupkg:
            nupkg_path = temp_nupkg.name

            # Создаем .nuspec файл
            nuspec_content = b"""<?xml version="1.0" encoding="utf-8"?>
            <package>
                <metadata>
                    <id>TestPackage</id>
                    <dependencies>
                        <dependency id="package1" version="1.0.0" />
                        <dependency id="package2" version="1.0.0" />
                    </dependencies>
                </metadata>
            </package>"""

            # Создаем zip-архив
            with zipfile.ZipFile(nupkg_path, 'w') as zf:
                zf.writestr('TestPackage.nuspec', nuspec_content)

        # Проверяем, что find_nuspec возвращает правильные зависимости
        expected_dependencies = ['TestPackage', 'package1 1.0', 'package2 1.0.0']
        result = m.find_nuspec(nupkg_path)
        self.assertEqual(result, expected_dependencies)

        # Удаляем временный файл
        os.remove(nupkg_path)


    def test_get_dependencies(self):
        nuspec_data = b'''
        <package>
            <metadata>
                <id>TestPackage</id>
                <dependencies>
                    <dependency id="Dependency1" version="1.0.0" />
                    <dependency id="Dependency2" version="2.0.0" />
                </dependencies>
            </metadata>
        </package>
        '''
        dependencies = m.get_dependencies(nuspec_data)
        self.assertEqual(dependencies, ['TestPackage', 'Dependency1 1.0.0', 'Dependency2 2.0.0'])

    def test_build_graph(self):
        dependencies = ['TestPackage', 'Dependency1 1.0.0', 'Dependency2 2.0.0']
        graph = m.build_graph(dependencies)

        expected_graph = 'graph TD\n\tA([TestPackage]) --> B1([Dependency1 1.0.0])\n\tA([TestPackage]) --> B2([Dependency2 2.0.0])\n'
        self.assertEqual(graph, expected_graph)

    @patch('builtins.open', new_callable=mock_open)
    def test_save_result(self, mock_file):
        m.save_result('test_result.md', 'test graph')
        mock_file.assert_called_once_with('test_result.md', 'w', encoding='utf-8')
        mock_file().write.assert_called_once_with('```\ntest graph\n```')

    @patch('builtins.open', new_callable=mock_open)
    def test_visualize_graph(self, mock_file):
        m.visualize_graph('visualizer.md', 'graph code')
        mock_file.assert_called_once_with('visualizer.md', 'w', encoding='utf-8')
        mock_file().write.assert_called_once_with('graph code')


if __name__ == '__main__':
    unittest.main()