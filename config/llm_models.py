"""
LLM模型配置和管理

这个模块负责管理不同的大语言模型配置，包括OpenAI、DeepSeek等模型的参数配置。
"""

from enum import Enum
from typing import Dict, Any, Optional
from dataclasses import dataclass
import logging

from config.settings import get_settings

# 获取配置
settings = get_settings()

# 配置日志
logger = logging.getLogger(__name__)


class LLMProvider(Enum):
    """LLM提供商枚举"""
    OPENAI = "openai"
    DEEPSEEK = "deepseek"
    ANTHROPIC = "anthropic"
    LOCAL = "local"


class ModelType(Enum):
    """模型类型枚举"""
    REASONING = "reasoning"    # 推理模型（如o1-preview）
    FAST = "fast"             # 快速模型（如gpt-4o-mini）
    ANALYSIS = "analysis"     # 分析模型
    CHAT = "chat"            # 对话模型


@dataclass
class ModelConfig:
    """模型配置数据类"""
    provider: LLMProvider
    model_name: str
    api_key: str
    base_url: str
    max_tokens: int = 2000
    temperature: float = 0.1
    timeout: int = 30
    max_retries: int = 3
    supports_function_calling: bool = False
    cost_per_1k_tokens: float = 0.0


class LLMModelManager:
    """LLM模型管理器"""
    
    def __init__(self):
        self._models: Dict[str, ModelConfig] = {}
        self._init_models()
    
    def _init_models(self):
        """初始化所有模型配置"""
        
        # OpenAI模型配置
        if settings.llm.openai_api_key:
            self._models.update({
                "gpt-4o": ModelConfig(
                    provider=LLMProvider.OPENAI,
                    model_name="gpt-4o",
                    api_key=settings.llm.openai_api_key,
                    base_url=settings.llm.openai_base_url,
                    max_tokens=4000,
                    temperature=0.1,
                    timeout=settings.llm.default_timeout,
                    max_retries=settings.llm.max_retries,
                    supports_function_calling=True,
                    cost_per_1k_tokens=0.03
                ),
                "gpt-4o-mini": ModelConfig(
                    provider=LLMProvider.OPENAI,
                    model_name="gpt-4o-mini",
                    api_key=settings.llm.openai_api_key,
                    base_url=settings.llm.openai_base_url,
                    max_tokens=2000,
                    temperature=0.1,
                    timeout=settings.llm.default_timeout,
                    max_retries=settings.llm.max_retries,
                    supports_function_calling=True,
                    cost_per_1k_tokens=0.0015
                ),
                "o1-preview": ModelConfig(
                    provider=LLMProvider.OPENAI,
                    model_name="o1-preview",
                    api_key=settings.llm.openai_api_key,
                    base_url=settings.llm.openai_base_url,
                    max_tokens=8000,
                    temperature=1.0,  # o1模型不支持调整temperature
                    timeout=60,  # 推理模型需要更长时间
                    max_retries=settings.llm.max_retries,
                    supports_function_calling=False,
                    cost_per_1k_tokens=0.15
                )
            })
        
        # DeepSeek模型配置
        if settings.llm.deepseek_api_key:
            self._models.update({
                "deepseek-chat": ModelConfig(
                    provider=LLMProvider.DEEPSEEK,
                    model_name="deepseek-chat",
                    api_key=settings.llm.deepseek_api_key,
                    base_url=settings.llm.deepseek_base_url,
                    max_tokens=4000,
                    temperature=0.1,
                    timeout=settings.llm.default_timeout,
                    max_retries=settings.llm.max_retries,
                    supports_function_calling=True,
                    cost_per_1k_tokens=0.002
                ),
                "deepseek-coder": ModelConfig(
                    provider=LLMProvider.DEEPSEEK,
                    model_name="deepseek-coder",
                    api_key=settings.llm.deepseek_api_key,
                    base_url=settings.llm.deepseek_base_url,
                    max_tokens=4000,
                    temperature=0.1,
                    timeout=settings.llm.default_timeout,
                    max_retries=settings.llm.max_retries,
                    supports_function_calling=True,
                    cost_per_1k_tokens=0.002
                )
            })
        
        # Anthropic模型配置
        if settings.llm.anthropic_api_key:
            self._models.update({
                "claude-3-sonnet": ModelConfig(
                    provider=LLMProvider.ANTHROPIC,
                    model_name="claude-3-sonnet-20240229",
                    api_key=settings.llm.anthropic_api_key,
                    base_url="https://api.anthropic.com",
                    max_tokens=4000,
                    temperature=0.1,
                    timeout=settings.llm.default_timeout,
                    max_retries=settings.llm.max_retries,
                    supports_function_calling=True,
                    cost_per_1k_tokens=0.015
                )
            })
        
        logger.info(f"初始化了 {len(self._models)} 个LLM模型")
    
    def get_model(self, model_name: str) -> Optional[ModelConfig]:
        """获取模型配置"""
        return self._models.get(model_name)
    
    def get_available_models(self) -> Dict[str, ModelConfig]:
        """获取所有可用模型"""
        return self._models.copy()
    
    def get_models_by_provider(self, provider: LLMProvider) -> Dict[str, ModelConfig]:
        """根据提供商获取模型"""
        return {
            name: config for name, config in self._models.items()
            if config.provider == provider
        }
    
    def get_models_by_type(self, model_type: ModelType) -> Dict[str, ModelConfig]:
        """根据类型获取推荐模型"""
        recommendations = {
            ModelType.REASONING: ["o1-preview", "gpt-4o"],
            ModelType.FAST: ["gpt-4o-mini", "deepseek-chat"],
            ModelType.ANALYSIS: ["gpt-4o", "claude-3-sonnet"],
            ModelType.CHAT: ["gpt-4o-mini", "deepseek-chat"]
        }
        
        recommended_models = recommendations.get(model_type, [])
        return {
            name: config for name, config in self._models.items()
            if name in recommended_models
        }
    
    def add_model(self, name: str, config: ModelConfig):
        """添加新模型配置"""
        self._models[name] = config
        logger.info(f"添加新模型: {name}")
    
    def remove_model(self, name: str):
        """移除模型配置"""
        if name in self._models:
            del self._models[name]
            logger.info(f"移除模型: {name}")


# 智能体角色对应的推荐模型
AGENT_MODEL_MAPPING = {
    # 分析师团队 - 需要深度分析能力
    "fundamental_analyst": "gpt-4o",
    "technical_analyst": "gpt-4o",
    "sentiment_analyst": "gpt-4o-mini",
    "news_analyst": "gpt-4o-mini",
    
    # 研究团队 - 需要推理和辩论能力
    "bullish_researcher": "o1-preview",
    "bearish_researcher": "o1-preview",
    "debate_facilitator": "gpt-4o",
    
    # 交易员 - 需要快速决策
    "trader": "gpt-4o",
    
    # 风险管理团队 - 需要严谨分析
    "risky_analyst": "gpt-4o",
    "neutral_analyst": "gpt-4o",
    "safe_analyst": "gpt-4o",
    "risk_facilitator": "gpt-4o",
    
    # 基金经理 - 需要综合判断
    "fund_manager": "o1-preview",
}


# 全局模型管理器实例
model_manager = LLMModelManager()


def get_model_config(model_name: str) -> Optional[ModelConfig]:
    """获取模型配置"""
    return model_manager.get_model(model_name)


def get_agent_model(agent_role: str) -> str:
    """根据智能体角色获取推荐模型"""
    return AGENT_MODEL_MAPPING.get(agent_role, "gpt-4o-mini")


def get_available_models() -> Dict[str, ModelConfig]:
    """获取所有可用模型"""
    return model_manager.get_available_models()


def estimate_cost(model_name: str, token_count: int) -> float:
    """估算模型调用成本"""
    config = get_model_config(model_name)
    if not config:
        return 0.0
    
    return (token_count / 1000) * config.cost_per_1k_tokens


def get_model_capabilities(model_name: str) -> Dict[str, Any]:
    """获取模型能力信息"""
    config = get_model_config(model_name)
    if not config:
        return {}
    
    return {
        "provider": config.provider.value,
        "max_tokens": config.max_tokens,
        "supports_function_calling": config.supports_function_calling,
        "cost_per_1k_tokens": config.cost_per_1k_tokens,
        "timeout": config.timeout,
        "max_retries": config.max_retries
    } 