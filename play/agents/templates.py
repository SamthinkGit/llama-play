from typing import Any, Optional

from haystack.agents.memory import ConversationMemory

from llama2terminal.base.agents.addons import ConversationalMemoryAddon
from llama2terminal.base.prompts.templates import Modules as mod
from llama2terminal.packages.play.agents.prompts import Modules as play
from llama2terminal.base.agents.templates import LlamaTemplateAgent
from llama2terminal.base.agents.build import LlamaModel

class LlamaPlayAgent(LlamaTemplateAgent):
    def __init__(self, game: str, max_msgs: Optional[int] = None) -> None:
        self.max_msgs = max_msgs
        self.game = game
        super().__init__()
    
    def build_model(self, fuse: Any | None = None) -> Any | None:
        llama = LlamaModel()
        llama.build_model(
            fuse=fuse,
            max_steps=1,
            memory=ConversationMemory(),
            addons=[ConversationalMemoryAddon(max_msgs=self.max_msgs)]
        )

        llama.prompt_generator.hard_params['GAME'] = self.game
        llama.prompt_generator.hard_params['EXAMPLE'] = play.EXAMPLES.EXAMPLE_GAME 

        llama.prompt_generator.modules += [
            play.BEHAVIOR.GAME_SIMULATOR_MODEL,
            play.TEMPLATES.GAME_SIMULATOR,
            mod.CHARACTERS.ONLY_ALPHANUMERIC_AND_EMOJIS,
            mod.SECURITY.CLOSE_PROMPT,
            mod.SECURITY.ANTI_BLOCK,
            play.SECURITY.BREAK_AFTER_OPTIONS,
        ]
        self.llama = llama

    def run(self, query: str, mute_active: bool = True) -> str:
        return self.llama.run(query=query, mute_active=mute_active)


    def free(self) -> None:
        self.llama.free()