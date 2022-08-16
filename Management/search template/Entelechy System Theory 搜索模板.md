
# 搜索模板


## 全局视图窗口排除无关文件夹

path:(-"attachment" -"code" -"Day Planners" -"History" -"Management" -"Papers" -"Projects" -"Reference" -"Resource")


## 全局视图窗口只选有关文件夹

path:("Theory" OR "Collection" OR "Design" OR "Notes" OR "Resource")



### 视图窗口显示青色

path:("Theory/EntelechySystem" OR "Theory/定义术语") OR tags:("#项目/EntelechySystem" OR "#内容/术语")


### 视图窗口显示绿色

path:("Theory/ComplexIntelligenceSystem " OR "Notes/机制" OR "Notes/机器功能" OR "Notes/硬件" OR "Notes/思维") OR tags:("tag:#项目/CIS" OR "tag:#内容/思维" OR "tag:#内容/认知" OR "tag:#内容/任务" OR "tag:#内容/决策" OR "tag:#内容/机制" OR "tag:#内容/功能" OR "#内容/机器")


### 视图窗口显示红色

path:("Theory/ElementalConceptionSystem" OR "Notes/意象" OR "Notes/语言" OR "Notes/概念" OR "Notes/语言") OR tags:("#项目/ECS" OR "#内容/玄学" OR "#内容/概念" OR "#内容/语言" OR "#内容/构式" OR "#内容/知识" OR "#内容/语义" OR "#内容/意象")


### 视图窗口显示橙黄色

path:("Theory/LifeManagementSystem" OR "Notes/个人与社会属性" OR "Notes/人生") OR tags:("#项目/LMS")



### 视图窗口显示蓝色

path:("Theory/AgentsWorldSystem" OR "Notes/多智能体" OR "Notes/世界") OR tags:("#项目/AWS")


## 局部视图窗口只选有关文件夹

path:("Theory" OR "Collection" OR "Design" OR "Notes" OR "Resource" OR "History")


### 局部视图窗口显示灰白色

path:History


