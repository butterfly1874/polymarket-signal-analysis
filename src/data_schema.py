"""
Polymarket信号分析 - 标准化数据Schema定义
Milestone 1 提交文件
功能：定义数据采集、存储、分析的标准化字段与数据校验规则
"""
from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional


class PolymarketDataSchema(BaseModel):
    """Polymarket核心数据标准化模型"""
    # 基础字段
    market_id: str = Field(..., description="市场唯一标识，如us-president-2024")
    timestamp: datetime = Field(..., description="数据采集时间（UTC+0）")

    # 赔率字段（0-1之间的浮点数）
    yes_price: float = Field(..., ge=0, le=1, description="YES选项赔率")
    no_price: float = Field(..., ge=0, le=1, description="NO选项赔率")

    # 交易量/流动性字段（非负）
    volume_24h: float = Field(..., ge=0, description="24小时成交量（USD）")
    liquidity: float = Field(..., ge=0, description="市场总流动性（USD）")

    # 分类与计算字段
    category: Optional[str] = Field(None, description="市场分类，如Politics/Sports")
    odds_change: Optional[float] = Field(None, description="5分钟赔率变动百分比")

    @validator('odds_change')
    def validate_odds_change(cls, v):
        """校验赔率变动百分比的合理性（-100到100之间）"""
        if v is not None and (v < -100 or v > 100):
            raise ValueError("赔率变动百分比需在-100到100之间")
        return v

    class Config:
        """配置：支持从字典导入数据，输出友好的错误信息"""
        populate_by_name = True
        error_msg_templates = {
            'value_error.number.not_ge': '字段{field_name}不能小于{limit_value}',
            'value_error.number.not_le': '字段{field_name}不能大于{limit_value}',
        }


# 测试用例：验证Schema有效性
if __name__ == "__main__":
    # 合法数据
    valid_data = {
        "market_id": "us-president-2024",
        "timestamp": datetime.utcnow(),
        "yes_price": 0.55,
        "no_price": 0.45,
        "volume_24h": 125000.0,
        "liquidity": 500000.0,
        "category": "Politics",
        "odds_change": 15.2
    }
    try:
        validated_data = PolymarketDataSchema(**valid_data)
        print("数据校验通过：", validated_data.dict())
    except ValueError as e:
        print("数据校验失败：", e)

    # 非法数据（赔率超出0-1范围）
    invalid_data = {
        "market_id": "us-president-2024",
        "timestamp": datetime.utcnow(),
        "yes_price": 1.2,  # 非法值
        "no_price": 0.45,
        "volume_24h": 125000.0,
        "liquidity": 500000.0,
        "odds_change": 200  # 非法值
    }
    try:
        PolymarketDataSchema(**invalid_data)
    except Exception as e:
        print("非法数据校验结果：", e)