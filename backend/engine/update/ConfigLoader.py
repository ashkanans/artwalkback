import json
import os


class ConfigLoader:
    @staticmethod
    def load_configs(config_path='backend\\scraper\\configs'):
        """
        Load JSON config files from the specified path.

        Parameters:
        - config_path: The path where JSON config files are located.

        Returns:
        - A list of loaded JSON objects.
        """
        tasks = []
        try:
            all_files = os.listdir(config_path)
            json_files = [file for file in all_files if file.endswith('.json')]
            for file_name in json_files:
                with open(os.path.join(config_path, file_name), 'r', encoding='utf-8') as file:
                    tasks.append(json.load(file))
            return tasks
        except FileNotFoundError:
            print(f"Error: The folder '{config_path}' does not exist.")
            return []
        except Exception as e:
            print(f"Failed to load configs. Exception: {e}")
            return []
