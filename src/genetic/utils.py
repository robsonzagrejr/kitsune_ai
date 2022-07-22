import dill
import copy


def save(result_save, file_path):
    try:
        result_save = copy.deepcopy(result_save)
        generation = result_save.get("generation", 0)
        print(f"Saving learning for generation {generation}")
        generation_file_name = f"{file_path}_generation_{generation}.dill"

        # Save Base
        with open(f"{file_path}.dill", 'wb+') as f:
            dill.dump(result_save, f)

        # Save Epoch
        with open(generation_file_name, 'wb+') as f:
            dill.dump(result_save, f)

    except Exception as e:
        print(f"Excetion: {e}")



def load(file_path):
    print("Loading learning...")
    result_load = None
    try:
        with open(f"{file_path}.dill", 'rb') as f:
            result_load = dill.load(f)
            generation = result_load.get("generation", 0)
            print(f"Learning from Generation {generation} Loaded")
    except Exception as e:
        print(f"Excetion: {e}")

    return result_load

