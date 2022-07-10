import pickle
import copy


def save(result_save, file_path):
    try:
        result_save = copy.deepcopy(result_save)
        epoch = result_save.get("epoch", 0)
        print(f"Saving learning for epoch {epoch}")
        epoch_file_name = f"{file_path}_epoch_{epoch}.pkl"

        # Save Base
        with open(f"{file_path}.pkl", 'wb+') as f:
            pickle.dump(result_save, f, protocol=pickle.HIGHEST_PROTOCOL)

        # Save Epoch
        with open(epoch_file_name, 'wb+') as f:
            pickle.dump(result_save, f, protocol=pickle.HIGHEST_PROTOCOL)

    except Exception as e:
        print(f"Excetion: {e}")



def load(file_path):
    print("Loading learning...")
    result_load = None
    try:
        with open(f"{file_path}.pkl", 'rb') as f:
            result_load = pickle.load(f)
            epoch = result_load.get("epoch", 0)
            print(f"Learning from Epoch {epoch} Loaded")
    except Exception as e:
        print(f"Excetion: {e}")

    return result_load

