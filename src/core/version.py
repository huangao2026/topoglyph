"""
版本管理系统
支持组件版本管理、兼容性检查、版本回滚和迁移
"""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
import re


class VersionComponent(Enum):
    """版本组件"""
    CORE = "core"                   # 核心系统
    PLUGIN = "plugin"               # 插件
    TOOL = "tool"                   # 工具
    MODEL = "model"                 # 模型
    CONFIG = "config"               # 配置
    SCHEMA = "schema"               # 数据库schema


@dataclass
class SemanticVersion:
    """语义化版本
    
    格式: MAJOR.MINOR.PATCH
    - MAJOR: 不兼容的API修改
    - MINOR: 向下兼容的功能性新增
    - PATCH: 向下兼容的问题修正
    """
    major: int
    minor: int
    patch: int
    prerelease: Optional[str] = None  # 预发布版本标识
    build_metadata: Optional[str] = None  # 构建元数据
    
    def __str__(self) -> str:
        """字符串表示"""
        version = f"{self.major}.{self.minor}.{self.patch}"
        if self.prerelease:
            version += f"-{self.prerelease}"
        if self.build_metadata:
            version += f"+{self.build_metadata}"
        return version
    
    def __eq__(self, other) -> bool:
        """版本相等"""
        if not isinstance(other, SemanticVersion):
            return False
        return (
            self.major == other.major and
            self.minor == other.minor and
            self.patch == other.patch and
            self.prerelease == other.prerelease
        )
    
    def __lt__(self, other) -> bool:
        """版本比较"""
        if not isinstance(other, SemanticVersion):
            return NotImplemented
        
        # 比较主版本号
        if self.major != other.major:
            return self.major < other.major
        
        # 比较次版本号
        if self.minor != other.minor:
            return self.minor < other.minor
        
        # 比较修订号
        if self.patch != other.patch:
            return self.patch < other.patch
        
        # 预发布版本比较
        if self.prerelease is None and other.prerelease is None:
            return False
        elif self.prerelease is None:
            return False  # 正式版本 > 预发布版本
        elif other.prerelease is None:
            return True
        else:
            return self.prerelease < other.prerelease
    
    def __le__(self, other) -> bool:
        """版本小于等于"""
        return self < other or self == other
    
    def __gt__(self, other) -> bool:
        """版本大于"""
        return not self <= other
    
    def __ge__(self, other) -> bool:
        """版本大于等于"""
        return not self < other
    
    @classmethod
    def parse(cls, version_str: str) -> 'SemanticVersion':
        """解析版本字符串
        
        Args:
            version_str: 版本字符串，如 "1.2.3", "2.0.0-alpha.1", "3.1.0+build.123"
            
        Returns:
            SemanticVersion: 版本对象
            
        Raises:
            ValueError: 版本格式无效
        """
        # 正则表达式匹配语义化版本
        pattern = r'^(\d+)\.(\d+)\.(\d+)(?:-([0-9A-Za-z-\.]+))?(?:\+([0-9A-Za-z-\.]+))?$'
        match = re.match(pattern, version_str)
        
        if not match:
            raise ValueError(f"Invalid semantic version: {version_str}")
        
        major = int(match.group(1))
        minor = int(match.group(2))
        patch = int(match.group(3))
        prerelease = match.group(4)
        build_metadata = match.group(5)
        
        return cls(major, minor, patch, prerelease, build_metadata)
    
    def is_compatible_with(self, other: 'SemanticVersion', allow_major_change: bool = False) -> bool:
        """检查版本兼容性
        
        Args:
            other: 另一个版本
            allow_major_change: 是否允许主版本号变化
            
        Returns:
            bool: 是否兼容
        """
        if allow_major_change:
            # 允许主版本号变化：只要求主版本号相同
            return self.major == other.major
        else:
            # 标准兼容性：主版本号必须相同，次版本号可以变化
            return self.major == other.major and self.minor <= other.minor


@dataclass
class VersionInfo:
    """版本信息"""
    component: VersionComponent          # 组件类型
    component_id: str                    # 组件ID
    version: SemanticVersion             # 版本号
    deployed_at: datetime = field(default_factory=datetime.now)  # 部署时间
    migration_hash: Optional[str] = None  # 迁移脚本哈希
    dependencies: Dict[str, str] = field(default_factory=dict)  # 依赖的组件版本
    metadata: Dict[str, Any] = field(default_factory=dict)       # 其他元数据
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "component": self.component.value,
            "component_id": self.component_id,
            "version": str(self.version),
            "deployed_at": self.deployed_at.isoformat(),
            "migration_hash": self.migration_hash,
            "dependencies": self.dependencies,
            "metadata": self.metadata
        }


@dataclass
class MigrationScript:
    """迁移脚本"""
    version_from: SemanticVersion
    version_to: SemanticVersion
    script_path: str
    checksum: str
    created_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "version_from": str(self.version_from),
            "version_to": str(self.version_to),
            "script_path": self.script_path,
            "checksum": self.checksum,
            "created_at": self.created_at.isoformat()
        }


class VersionManager:
    """版本管理器
    
    管理系统各组件的版本，提供版本查询、兼容性检查、迁移和回滚功能
    """
    
    def __init__(self):
        self._versions: Dict[str, List[VersionInfo]] = {}  # component_id -> version_history
        self._current_versions: Dict[str, VersionInfo] = {}  # component_id -> current_version
        self._migration_scripts: List[MigrationScript] = []
    
    def register_version(self, version_info: VersionInfo):
        """注册版本
        
        Args:
            version_info: 版本信息
        """
        component_key = f"{version_info.component.value}:{version_info.component_id}"
        
        if component_key not in self._versions:
            self._versions[component_key] = []
        
        self._versions[component_key].append(version_info)
        self._current_versions[component_key] = version_info
    
    def get_current_version(self, component: VersionComponent, component_id: str) -> Optional[VersionInfo]:
        """获取当前版本
        
        Args:
            component: 组件类型
            component_id: 组件ID
            
        Returns:
            Optional[VersionInfo]: 当前版本信息
        """
        component_key = f"{component.value}:{component_id}"
        return self._current_versions.get(component_key)
    
    def get_version_history(self, component: VersionComponent, component_id: str) -> List[VersionInfo]:
        """获取版本历史
        
        Args:
            component: 组件类型
            component_id: 组件ID
            
        Returns:
            List[VersionInfo]: 版本历史列表
        """
        component_key = f"{component.value}:{component_id}"
        return self._versions.get(component_key, [])
    
    def check_compatibility(
        self,
        component1: VersionComponent,
        component_id1: str,
        component2: VersionComponent,
        component_id2: str,
        allow_major_change: bool = False
    ) -> bool:
        """检查两个组件的版本兼容性
        
        Args:
            component1: 第一个组件类型
            component_id1: 第一个组件ID
            component2: 第二个组件类型
            component_id2: 第二个组件ID
            allow_major_change: 是否允许主版本号变化
            
        Returns:
            bool: 是否兼容
        """
        version1 = self.get_current_version(component1, component_id1)
        version2 = self.get_current_version(component2, component_id2)
        
        if not version1 or not version2:
            return False
        
        # 检查依赖关系
        if component2.value in version1.dependencies:
            required_version = SemanticVersion.parse(version1.dependencies[component2.value])
            if not version2.version.is_compatible_with(required_version):
                return False
        
        return version1.version.is_compatible_with(version2.version, allow_major_change)
    
    def add_migration_script(self, script: MigrationScript):
        """添加迁移脚本
        
        Args:
            script: 迁移脚本
        """
        self._migration_scripts.append(script)
    
    def find_migration_path(
        self,
        from_version: SemanticVersion,
        to_version: SemanticVersion
    ) -> List[MigrationScript]:
        """查找迁移路径
        
        Args:
            from_version: 起始版本
            to_version: 目标版本
            
        Returns:
            List[MigrationScript]: 迁移脚本列表
        """
        path = []
        current = from_version
        
        while current != to_version:
            # 查找从当前版本到下一个版本的迁移脚本
            found = False
            for script in self._migration_scripts:
                if script.version_from == current:
                    path.append(script)
                    current = script.version_to
                    found = True
                    break
            
            if not found:
                return []  # 找不到迁移路径
        
        return path
    
    async def rollback_to_version(
        self,
        component: VersionComponent,
        component_id: str,
        target_version: SemanticVersion
    ) -> bool:
        """回滚到指定版本
        
        Args:
            component: 组件类型
            component_id: 组件ID
            target_version: 目标版本
            
        Returns:
            bool: 是否成功
        """
        current = self.get_current_version(component, component_id)
        if not current:
            return False
        
        if current.version == target_version:
            return True  # 已经是目标版本
        
        # 查找目标版本是否存在于历史记录中
        history = self.get_version_history(component, component_id)
        target_version_info = None
        for version_info in reversed(history):
            if version_info.version == target_version:
                target_version_info = version_info
                break
        
        if not target_version_info:
            return False  # 目标版本不存在
        
        # 查找回滚迁移路径
        # TODO: 实现回滚迁移
        
        # 更新当前版本
        component_key = f"{component.value}:{component_id}"
        self._current_versions[component_key] = target_version_info
        
        return True
    
    def get_system_version_report(self) -> Dict[str, Any]:
        """获取系统版本报告"""
        report = {
            "components": {},
            "timestamp": datetime.now().isoformat()
        }
        
        for component_key, version_info in self._current_versions.items():
            report["components"][component_key] = version_info.to_dict()
        
        return report


class CompatibilityError(Exception):
    """版本兼容性错误"""
    pass


class MigrationError(Exception):
    """迁移错误"""
    pass


class VersionNotFoundError(Exception):
    """版本不存在错误"""
    pass
