from abc import ABC, abstractmethod


class IRenderer(ABC):

    @abstractmethod
    def render(self, template_path, **kwargs) -> str:
        pass
    
    @abstractmethod
    def exits_template(self, template_path) -> bool:
        pass