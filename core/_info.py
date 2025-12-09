# ==== 模块信息 ==== #
# 版本号规则
# { PARADIGM } . { REFACTORING } . { MAINTENANCE } . { BUGFIX } 
# 如果一次修改涉及了主要使用范式的变化
# 就更新PARADIGM
# 如果一次修改涉及了重大代码重构，或是优化
# 以至于无法兼容某些旧版数据格式
# 就增加REFACTORING
# 如果一次修改仅涉及了小改动
# 比如修复了某些bug，或是添加了某些小功能
# 亦或是改动不会导致部署上的巨大影响
# 就增加MAINTENANCE
# 如果只是单纯的修复了一些小Bug
# 或是提升了某些地方的性能
# 而不涉及代码逻辑的改变
# 就增加BUGFIX
# 
# 上一级别的变化会清零后面的所有版本号
# 接口版本号与核心版本号是两个独立的版本号
# 接口版本号不变的情况下接口大概率是不变的
__version__ = "4.3.3.9"

__author__ = "Qeggs"
__license__ = "MIT"
__copyright__ = "Copyright (c) 2025 Qeggs"