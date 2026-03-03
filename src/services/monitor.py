"""
监控和指标系统
收集系统运行指标，提供性能监控和健康检查
"""
import time
from collections import defaultdict, deque
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Callable, Dict, List, Optional
import asyncio


class MetricType(Enum):
    """指标类型"""
    COUNTER = "counter"             # 计数器（只增不减）
    GAUGE = "gauge"                 # 仪表（可增可减）
    HISTOGRAM = "histogram"         # 直方图（分布统计）
    SUMMARY = "summary"             # 摘要（统计信息）


@dataclass
class Metric:
    """指标基类"""
    name: str                       # 指标名称
    type: MetricType                # 指标类型
    description: str                # 描述
    labels: Dict[str, str] = field(default_factory=dict)  # 标签
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class CounterMetric(Metric):
    """计数器指标"""
    value: float = 0.0
    
    def increment(self, value: float = 1.0):
        """增加计数"""
        if value < 0:
            raise ValueError("Counter can only be incremented")
        self.value += value


@dataclass
class GaugeMetric(Metric):
    """仪表指标"""
    value: float = 0.0
    
    def set(self, value: float):
        """设置值"""
        self.value = value
    
    def increment(self, value: float = 1.0):
        """增加值"""
        self.value += value
    
    def decrement(self, value: float = 1.0):
        """减少值"""
        self.value -= value


@dataclass
class HistogramMetric(Metric):
    """直方图指标"""
    buckets: List[float]            # 桶边界
    bucket_counts: Dict[float, int] = field(default_factory=dict)
    sum: float = 0.0
    count: int = 0
    
    def __post_init__(self):
        """初始化桶计数"""
        for bucket in self.buckets:
            self.bucket_counts[bucket] = 0
        self.bucket_counts["+Inf"] = 0
    
    def observe(self, value: float):
        """观察一个值"""
        # 找到合适的桶
        for bucket in sorted(self.buckets):
            if value <= bucket:
                self.bucket_counts[bucket] += 1
            else:
                break
        
        # 更新+Inf桶
        self.bucket_counts["+Inf"] += 1
        
        # 更新总和和计数
        self.sum += value
        self.count += 1


@dataclass
class SummaryMetric(Metric):
    """摘要指标"""
    values: deque = field(default_factory=lambda: deque(maxlen=1000))
    sum: float = 0.0
    count: int = 0
    
    def observe(self, value: float):
        """观察一个值"""
        self.values.append(value)
        self.sum += value
        self.count += 1
    
    def get_quantile(self, quantile: float) -> float:
        """获取分位数"""
        if not self.values:
            return 0.0
        
        sorted_values = sorted(self.values)
        index = int(quantile * len(sorted_values))
        return sorted_values[min(index, len(sorted_values) - 1)]


class MetricsCollector:
    """指标收集器"""
    
    def __init__(self):
        self._metrics: Dict[str, Metric] = {}
    
    def register_counter(
        self,
        name: str,
        description: str,
        labels: Optional[Dict[str, str]] = None
    ) -> CounterMetric:
        """注册计数器指标"""
        metric = CounterMetric(
            name=name,
            type=MetricType.COUNTER,
            description=description,
            labels=labels or {}
        )
        self._metrics[name] = metric
        return metric
    
    def register_gauge(
        self,
        name: str,
        description: str,
        labels: Optional[Dict[str, str]] = None
    ) -> GaugeMetric:
        """注册仪表指标"""
        metric = GaugeMetric(
            name=name,
            type=MetricType.GAUGE,
            description=description,
            labels=labels or {}
        )
        self._metrics[name] = metric
        return metric
    
    def register_histogram(
        self,
        name: str,
        description: str,
        buckets: Optional[List[float]] = None,
        labels: Optional[Dict[str, str]] = None
    ) -> HistogramMetric:
        """注册直方图指标"""
        if buckets is None:
            buckets = [0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0]
        
        metric = HistogramMetric(
            name=name,
            type=MetricType.HISTOGRAM,
            description=description,
            buckets=buckets,
            labels=labels or {}
        )
        self._metrics[name] = metric
        return metric
    
    def register_summary(
        self,
        name: str,
        description: str,
        labels: Optional[Dict[str, str]] = None
    ) -> SummaryMetric:
        """注册摘要指标"""
        metric = SummaryMetric(
            name=name,
            type=MetricType.SUMMARY,
            description=description,
            labels=labels or {}
        )
        self._metrics[name] = metric
        return metric
    
    def get_metric(self, name: str) -> Optional[Metric]:
        """获取指标"""
        return self._metrics.get(name)
    
    def list_metrics(self) -> List[Metric]:
        """列出所有指标"""
        return list(self._metrics.values())
    
    def export_metrics(self) -> str:
        """导出指标为 Prometheus 格式"""
        lines = []
        
        for metric in self._metrics.values():
            # 添加指标描述
            lines.append(f"# HELP {metric.name} {metric.description}")
            lines.append(f"# TYPE {metric.name} {metric.type.value}")
            
            # 添加指标值
            if isinstance(metric, CounterMetric):
                lines.append(f"{metric.name} {metric.value}")
            elif isinstance(metric, GaugeMetric):
                lines.append(f"{metric.name} {metric.value}")
            elif isinstance(metric, HistogramMetric):
                lines.append(f"{metric.name}_sum {metric.sum}")
                lines.append(f"{metric.name}_count {metric.count}")
                for bucket, count in metric.bucket_counts.items():
                    lines.append(f'{metric.name}_bucket{{le="{bucket}"}} {count}')
            elif isinstance(metric, SummaryMetric):
                lines.append(f"{metric.name}_sum {metric.sum}")
                lines.append(f"{metric.name}_count {metric.count}")
        
        return "\n".join(lines)


class PerformanceMonitor:
    """性能监控器"""
    
    def __init__(self, metrics_collector: MetricsCollector):
        self._metrics = metrics_collector
        
        # 注册默认指标
        self._request_count = self._metrics.register_counter(
            "requests_total",
            "Total number of requests"
        )
        self._request_duration = self._metrics.register_histogram(
            "request_duration_seconds",
            "Request duration in seconds"
        )
        self._active_requests = self._metrics.register_gauge(
            "active_requests",
            "Number of active requests"
        )
        self._error_count = self._metrics.register_counter(
            "errors_total",
            "Total number of errors"
        )
    
    async def track_request(self, func: Callable, *args, **kwargs) -> Any:
        """跟踪请求
        
        Args:
            func: 要执行的函数
            *args: 位置参数
            **kwargs: 关键字参数
            
        Returns:
            Any: 函数返回值
        """
        self._active_requests.increment()
        start_time = time.time()
        
        try:
            self._request_count.increment()
            result = await func(*args, **kwargs)
            
            # 记录请求持续时间
            duration = time.time() - start_time
            self._request_duration.observe(duration)
            
            return result
        
        except Exception as e:
            # 记录错误
            self._error_count.increment()
            raise
        
        finally:
            self._active_requests.decrement()


class HealthChecker:
    """健康检查器"""
    
    def __init__(self, event_bus):
        self._event_bus = event_bus
        self._health_checks: Dict[str, Callable] = {}
    
    def register_health_check(self, name: str, check_func: Callable):
        """注册健康检查
        
        Args:
            name: 检查名称
            check_func: 检查函数，返回 Dict[str, Any]
        """
        self._health_checks[name] = check_func
    
    async def check_health(self) -> Dict[str, Any]:
        """执行所有健康检查
        
        Returns:
            Dict: 健康状态
        """
        results = {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "checks": {}
        }
        
        unhealthy_count = 0
        
        for name, check_func in self._health_checks.items():
            try:
                result = await check_func()
                results["checks"][name] = result
                
                if result.get("status") != "healthy":
                    unhealthy_count += 1
            except Exception as e:
                results["checks"][name] = {
                    "status": "error",
                    "error": str(e)
                }
                unhealthy_count += 1
        
        # 确定总体状态
        if unhealthy_count > 0:
            results["status"] = "unhealthy"
        
        return results
    
    async def check_component(self, name: str) -> Optional[Dict[str, Any]]:
        """检查单个组件"""
        check_func = self._health_checks.get(name)
        if check_func:
            try:
                return await check_func()
            except Exception as e:
                return {
                    "status": "error",
                    "error": str(e)
                }
        return None


class AlertManager:
    """告警管理器"""
    
    def __init__(self):
        self._rules: List[Dict[str, Any]] = []
        self._alerts: deque = deque(maxlen=100)
    
    def add_rule(
        self,
        name: str,
        condition: Callable[[Dict[str, Any]], bool],
        severity: str = "warning",
        action: Optional[Callable] = None
    ):
        """添加告警规则
        
        Args:
            name: 规则名称
            condition: 条件函数
            severity: 严重程度
            action: 触发动作
        """
        self._rules.append({
            "name": name,
            "condition": condition,
            "severity": severity,
            "action": action
        })
    
    async def evaluate(self, metrics: Dict[str, Any]):
        """评估告警规则
        
        Args:
            metrics: 指标数据
        """
        for rule in self._rules:
            try:
                if rule["condition"](metrics):
                    alert = {
                        "rule_name": rule["name"],
                        "severity": rule["severity"],
                        "timestamp": datetime.now().isoformat(),
                        "metrics": metrics
                    }
                    
                    self._alerts.append(alert)
                    
                    # 执行触发动作
                    if rule["action"]:
                        await rule["action"](alert)
            except Exception as e:
                print(f"Error evaluating alert rule {rule['name']}: {e}")
    
    def get_recent_alerts(self, count: int = 10) -> List[Dict[str, Any]]:
        """获取最近的告警"""
        return list(self._alerts)[-count:]


class SystemMonitor:
    """系统监控
    
    整合指标收集、性能监控、健康检查和告警
    """
    
    def __init__(self, event_bus):
        self._event_bus = event_bus
        self._metrics_collector = MetricsCollector()
        self._performance_monitor = PerformanceMonitor(self._metrics_collector)
        self._health_checker = HealthChecker(event_bus)
        self._alert_manager = AlertManager()
        
        # 注册默认健康检查
        self._register_default_health_checks()
        
        # 注册默认告警规则
        self._register_default_alerts()
    
    def _register_default_health_checks(self):
        """注册默认健康检查"""
        # TODO: 添加更多健康检查
        pass
    
    def _register_default_alerts(self):
        """注册默认告警规则"""
        # 错误率告警
        self._alert_manager.add_rule(
            name="high_error_rate",
            condition=lambda m: m.get("errors_total", 0) / max(m.get("requests_total", 1), 1) > 0.1,
            severity="critical"
        )
    
    def get_metrics_collector(self) -> MetricsCollector:
        """获取指标收集器"""
        return self._metrics_collector
    
    def get_performance_monitor(self) -> PerformanceMonitor:
        """获取性能监控器"""
        return self._performance_monitor
    
    def get_health_checker(self) -> HealthChecker:
        """获取健康检查器"""
        return self._health_checker
    
    def get_alert_manager(self) -> AlertManager:
        """获取告警管理器"""
        return self._alert_manager
    
    async def get_system_status(self) -> Dict[str, Any]:
        """获取系统状态"""
        health_status = await self._health_checker.check_health()
        metrics = self._metrics_collector.export_metrics()
        alerts = self._alert_manager.get_recent_alerts()
        
        return {
            "health": health_status,
            "metrics": metrics,
            "alerts": alerts
        }
