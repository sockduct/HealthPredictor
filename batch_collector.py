#! /usr/bin/env python


# Standard Library
import argparse
import asyncio
from copy import deepcopy
from datetime import datetime
from pathlib import Path
import sys
import time

# 3rd Party
from nbclient import NotebookClient
from nbformat import read, write, v4


# Platform-specifics:
if sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


def inject_parameters(nb, parameters):
    '''Injects a new cell at the top of the notebook with parameter definitions.'''
    param_code = '\n'.join(f'{k} = {repr(v)}' for k, v in parameters.items())
    param_cell = v4.new_code_cell(source=param_code)

    # Insert at top or replace a cell tagged 'parameters'
    # Optional: look for existing 'parameters' tag and replace instead
    nb.cells.insert(0, param_cell)

    return nb


def clear_outputs(nb):
    for cell in nb.cells:
        if 'outputs' in cell:
            cell['outputs'] = []
        if 'execution_count' in cell:
            cell['execution_count'] = None

    return nb


def get_args() -> argparse.Namespace:
    # Setup argument parsing
    parser = argparse.ArgumentParser(
                description='Run a notebook multiple times to collect results from each run.',
                epilog="Don't forget to setup a runtime variables to distinguish each run.",
    )
    # Add (root) positional argument, default type is str, can change
    # parser.add_argument('name', help='name of the person to greet', type=str)
    # Add (root) optional argument(s)
    parser.add_argument('notebook', default='', help='Jupyter Notebook to run')
    parser.add_argument('-t', '--times', default=1, type=int, help='how many times to run notebook')

    return parser.parse_args()


def main(notebook: str, times: int) -> None:
    cwd = Path(notebook).parent
    if not (nb_path := (cwd/notebook).is_file()) and not (nb_path := cwd/f'{notebook}.ipynb'):
        raise FileNotFoundError(f'Could not find notebook: {notebook}')

    # Read in notebook:
    with open(nb_path, encoding='utf-8') as f:
        original_nb = read(f, as_version=4)

    # Clean notebook:
    clean_nb = clear_outputs(original_nb)

    for i in range(times):
        run_start = time.perf_counter()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f'🔄 Run {i+1}/{times} started at {timestamp}...', end='', flush=True)

        nb_copy = deepcopy(clean_nb)

        # Inject params (e.g., run_id):
        nb_with_params = inject_parameters(nb_copy, {'run_id': i})

        client = NotebookClient(nb_with_params, timeout=600, kernel_name='python3')
        client.execute()

        # Run the notebook in-memory:
        try:
            client = NotebookClient(nb_with_params, timeout=600, kernel_name='python3')
            client.execute()

            run_end = time.perf_counter()
            duration = run_end - run_start
            minutes, seconds = divmod(duration, 60)
            print(f'✅ Run {i+1}/{times} finished in {int(minutes)}m {seconds:.2f}s', flush=True)
        except Exception as e:
            run_end = time.perf_counter()
            duration = run_end - run_start
            minutes, seconds = divmod(duration, 60)
            print(
                f'❌ Run {i+1}/{times} failed after {int(minutes)}m {seconds:.2f}s: {e}',
                flush=True
            )


if __name__ == '__main__':
    args = get_args()
    main(args.notebook, args.times)
