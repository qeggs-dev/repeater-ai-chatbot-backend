from dataclasses import dataclass, field, asdict

@dataclass
class BrowserStats:
    """浏览器池统计信息"""
    total_browsers: int = 0
    available_browsers: int = 0
    total_pages: int = 0
    available_pages: int = 0
    browser_type_counts: dict[str, int] = field(default_factory=dict)
    
    def __str__(self) -> str:
        return (
            f"Browsers: {self.available_browsers}/{self.total_browsers} available | "
            f"Pages: {self.available_pages}/{self.total_pages} available"
        )
    
    @property
    def as_dict(self) -> dict[str, int | dict[str, int]]:
        return asdict(self)