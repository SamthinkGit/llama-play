from llama2terminal.packages.play.agents.templates import LlamaPlayAgent
from llama2terminal.config.sysutils import TerminalColors as c, typing_print
import sys
import traceback
import gc
import torch

def __start__(args):
    
    if len(args) == 1:
        print("Use <llama play [GAME]> to start simulating the game requested")
        return

    game = args[1]
    print(f"Loading SIMULATION for {game}...")
    sys.stdout.flush()

    llama = LlamaPlayAgent(game, max_msgs=2)
    llama.build_model()

    print(f"{c.ORANGE}==== GAME_SIMULATION, use 'exit' to escape ===={c.ENDC}")
    try:
        torch.cuda.empty_cache()
        output = llama.run(query=f"Start the simulation of the game {game}, remember to give a quick welcome to the human and let him start playing",mute_active=False)
        typing_print(f"{c.BLUE}({game}): {output}{c.ENDC}\n")

        while True:

            torch.cuda.empty_cache()
            query = input(f"> ")
            if query == "exit":
                free(llama)
                break

            output = llama.run(query=query,mute_active=False)
            typing_print(f"{c.BLUE}({game}): {output}{c.ENDC}\n")
    
    except Exception as e:
        traceback.print_exc()
        free(llama)
        
def free(llama):
    llama.free()
    llama = None
    gc.collect()
    torch.cuda.empty_cache()
