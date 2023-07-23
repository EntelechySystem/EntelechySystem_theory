"""功能函数集：计算构建个体与个体间相关状态及其转换。"""

from . import np
from .core.define.define_agents import Agent, AgentInteragent
from .core.define.define_consts import *
from .core.define.define_environmentVariables import env
from .core.define.define_type import StateType

pass  # end import


class AgentState:
    agent: Agent
    interagent: AgentInteragent

    ## 【状态数量】`num_states`
    num_states: int

    ## 【状态集合列表】`states_list`
    states_list: list

    ## 【状态数据集合列表】`states_data_list`
    states_data_list: list

    ## 【交互状态数据集合列表】`interstates_data_list`
    interstates_data_list: list

    ## 【计算状态函数集合列表】`calc_state_functions_list`
    calc_state_functions_list: np.array

    ## 【计算状态函数集合字典集】`calc_state_functions_dicts`
    calc_state_functions_dicts: dict

    ## 【状态关系集合列表01】`state_relations_list_01`
    state_relations_list_01: list

    ## 【状态关系集合列表02】`state_relations_list_02`
    state_relations_list_02: list

    ## 【状态关系邻接矩阵01】`state_relations_adjacent_matrix_01`
    state_relations_adjacent_matrix_01: np.array

    ## 【状态关系邻接矩阵02】`state_relations_adjacent_matrix_02`
    state_relations_adjacent_matrix_02: np.array

    ## 【状态关系实体编号邻接矩阵】`state_relation_entities_adjacent_matrix`
    ## 用于标记、区别具体的多状态关系，避免发生混淆。其中编号`0`是特殊编号，表示没有特殊标记。
    ## 例如对于同一个汇状态`s_t0`，有两个状态关系`s_t0 = s_t1 + s_t2`和`s_t0 = s_t3 + s_t4`，则这两个状态关系在矩阵中，`s_t1`与`s_t2`之实体编号均为`1`，`s_t3`与`s_t4`之实体编号均为`2`。
    state_relation_entities_adjacent_matrix: np.array

    ## 【状态实体索引列表】`state_entity_indices_list`。
    ## 列表之每一个元素是一个子列表。子列表描述了矩阵每一列之情况。子列表每一个元素是一个字典。
    ## 字典统计了`state_relation_entities_adjacent_matrix`与`state_relations_adjacent_matrix_02`对应的。
    ## 字典之键是`state_relation_entities_adjacent_matrix`之列之唯一值，字典之值是该唯一值所在索引构成的列表。
    state_entity_indices_list: list

    ## 【更新状态函数集合列表01】`update_state_functions_list_01`
    update_state_functions_list_01: list

    ## 【更新状态函数字典集01】`update_state_functions_dicts_01`
    update_state_functions_dicts_01: dict

    ## 【更新状态函数邻接字典】`update_state_functions_adjacent_dicts_01`
    update_state_functions_adjacent_dicts_01: dict

    ## 【更新状态函数集合列表02】`update_state_functions_list_02`
    update_state_functions_list_02: list

    ## 【更新状态函数字典02】`update_state_functions_dicts_02`
    update_state_functions_dicts_02: dict

    ## 【更新状态关系函数邻接矩阵01】`update_state_functions_adjacent_matrix_01`
    update_state_functions_adjacent_matrix_01: np.array

    ## 【更新状态关系函数邻接矩阵02】`update_state_functions_adjacent_matrix_02`
    update_state_functions_adjacent_matrix_02: np.array

    ## 【状态关系索引表】`states_relations_indices_table`
    states_relations_indices_table: list

    @classmethod
    def build_state_const_variables(cls, agent: Agent, interagent: AgentInteragent):
        """
        构建各类状态常量变量。
        
        Args:
            agent(Agent): 个体个体众；
            interagent(AgentInteragent): 个体间个体众；
        
        Returns:
    
        """

        cls.agent = agent
        cls.interagent = interagent

        ## 设置【状态集合列表】`states_list`
        cls.states_list = [
            'on',
            'hel',
            'isv',
            'ilq',
            'br',
            'off',
        ]

        cls.num_states = len(cls.states_list)

        ## 设置【状态集合数据列表】`states_data_list` 
        cls.states_data_list = [
            cls.agent.on,
            cls.agent.hel,
            cls.agent.isv,
            cls.agent.ilq,
            cls.agent.br,
            cls.agent.off,
        ]

        ## 设置【交互状态集合数据列表】`interstates_data_list`
        cls.interstates_data_list = [
            cls.interagent.on,
            cls.interagent.hel,
            cls.interagent.isv,
            cls.interagent.ilq,
            cls.interagent.br,
            cls.interagent.off,
        ]

        ## 【计算状态函数集合列表】`calc_state_functions_list`
        cls.calc_state_functions_list = [
            cls.calc_state_on,
            cls.calc_state_hel,
            cls.calc_state_isv,
            cls.calc_state_ilq,
            cls.calc_state_br,
            cls.calc_state_off
        ]

        ## 【计算状态函数集合字典集】`calc_state_functions_dicts`
        cls.calc_state_functions_dicts = dict(zip(cls.states_list, cls.calc_state_functions_list))

        ## 构建【源状态网格矩阵】`source_states_grid_matrix`、【汇状态网格矩阵】（笛卡尔积矩阵）`target_states_grid_matrix`
        cls.source_states_grid_matrix, cls.target_states_grid_matrix = np.meshgrid(cls.states_list, cls.states_list, indexing='ij')

        ## 设置【状态关系集合列表01】`state_relations_list_01`
        ## 同一种状态标记【同】；
        ## 手动更新标记【手】；
        ## 不存在直接关系标记【无】；
        ## 非确定的关系标记【疑】；
        ## 包含关系，标记【母】
        ## 被包含关系，标记【子】；
        ## 互相排斥关系，标记【非】；
        ## 其它可以推导关系，标记【推】；
        ## 全部的相关的源状态全部都是假，汇状态才是真。先非运算，再与运算关系，标记【非与】；
        cls.state_relations_list_01 = [
            '同',
            '手',
            '无',
            '疑',
            '母',
            '子',
            '斥',
            '非',
        ]

        ## 设置【更新状态函数集合列表01】`update_state_functions_list_01`
        cls.update_state_functions_list_01 = [
            cls.update_state_if_equity,
            cls.update_state_if_handle,
            cls.update_state_if_none,
            cls.update_state_if_uncertain,
            cls.update_state_if_parent,
            cls.update_state_if_child,
            cls.update_state_if_exclusive,
            cls.update_state_if_nand,
        ]

        ## 设置【状态关系邻接矩阵01】`state_relations_adjacent_matrix_01`
        cls.state_relations_adjacent_matrix_01 = [
            ['同', '母', '母', '母', '母', '斥', ],
            ['子', '同', '疑', '疑', '无', '无', ],
            ['子', '非', '同', '无', '手', '无', ],
            ['子', '非', '无', '同', '手', '无', ],
            ['子', '无', '疑', '疑', '同', '手', ],
            ['斥', '无', '无', '无', '无', '同', ],
        ]

        ## 设置【状态关系邻接矩阵02】`state_relations_adjacent_matrix_02`
        cls.state_relations_adjacent_matrix_02 = np.array([
            ['无', '无', '无', '无', '无', '无', ],
            ['无', '无', '无', '无', '无', '无', ],
            ['无', '与', '无', '无', '无', '无', ],
            ['无', '与', '无', '无', '无', '无', ],
            ['无', '无', '无', '无', '无', '无', ],
            ['无', '无', '无', '无', '无', '无', ],
        ])

        ## 设置【状态关系实体编号邻接矩阵】`state_relation_entities_adjacent_matrix`
        cls.state_relation_entities_adjacent_matrix = np.array([
            [0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 0, ],
            [0, 1, 0, 0, 0, 0, ],
            [0, 1, 0, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 0, ],
        ])

        ## 设置状态关系集合列表02`state_relations_list_02`
        ## 不存在直接关系标记【无】；
        ## 全部的相关的源状态全部都是假，汇状态才是真。先非运算，再与运算关系，标记【非与】；
        cls.state_relations_list_02 = [
            '无',
            '与',
        ]

        ## 设置【更新状态函数集合列表02】`update_state_functions_list_02`
        cls.update_state_functions_list_02 = [
            cls.update_target_state_if_none,
            cls.update_target_state_if_and,
        ]

        # ## 构建【状态关系索引表】`states_relations_indices_table` #HACK 暂时用不到
        # cls.states_relations_indices_table = np.column_stack([cls.source_states_grid_matrix.ravel(), cls.target_states_grid_matrix.ravel(), np.asarray(cls.state_relations_adjacent_matrix_01).ravel()])

        ## 构建【更新状态函数字典集01】`update_state_functions_dicts_01`
        cls.update_state_functions_dicts_01 = dict(zip(cls.state_relations_list_01, cls.update_state_functions_list_01))

        ## 设置更新状态函数字典集02`update_state_functions_dicts_02`
        cls.update_state_functions_dicts_02 = dict(zip(cls.state_relations_list_02, cls.update_state_functions_list_02))

        ## 根据`state_relations_adjacent_matrix_01`构建update_state_functions_adjacent_matrix_01`。矩阵每个元素是一个更新状态函数，对应【状态关系邻接矩阵01】`state_relations_adjacent_matrix_01`之元素之状态关系名。。
        cls.update_state_functions_adjacent_matrix_01 = np.empty((cls.num_states, cls.num_states), dtype=object)
        for i, row in enumerate(cls.state_relations_adjacent_matrix_01):
            for j, col in enumerate(row):
                cls.update_state_functions_adjacent_matrix_01[i, j] = cls.update_state_functions_dicts_01[col]

        ## 根据`state_relations_adjacent_matrix_02`构建`update_state_functions_adjacent_matrix_02`。数组每个元素是一个更新汇状态函数，对应【状态关系邻接矩阵02】`state_relations_adjacent_matrix_02`之元素之状态关系名。
        cls.update_state_functions_adjacent_matrix_02 = np.empty((cls.num_states, cls.num_states), dtype=object)
        for i, row in enumerate(cls.state_relations_adjacent_matrix_02):
            for j, col in enumerate(row):
                cls.update_state_functions_adjacent_matrix_02[i, j] = cls.update_state_functions_dicts_02[col]

        ## 构建【状态实体索引列表】`state_entity_indices_list`，根据【状态关系实体编号邻接矩阵】`state_relation_entities_adjacent_matrix`与【状态关系邻接矩阵02】`state_relations_adjacent_matrix_02`。
        ## 列表之每一个元素是一个子列表。子列表描述了矩阵每一列之情况。子列表每一个元素是一个四元组。
        ## 四元组统计了`state_relation_entities_adjacent_matrix`与`state_relations_adjacent_matrix_02`对应的信息。
        ## 四元组之第一个元素与第二个元素一一对应。它们分别是`state_relation_entities_adjacent_matrix`、`state_relations_adjacent_matrix_02`之列之唯一的值。
        ## 第三个元素是`state_relations_adjacent_matrix_02`之列之唯一的值作为键，对应字典`update_state_functions_dicts_02`之值。
        ## 第四个元素是`state_relation_entities_adjacent_matrix`之列之唯一值所在索引构成的列表。
        ## 第五个元素是`state_relation_entities_adjacent_matrix`之列值。
        cls.state_entity_indices_list = []
        for j in range(cls.num_states):
            unique_vals = np.unique(cls.state_relation_entities_adjacent_matrix[:, j])
            for val in unique_vals:
                entity_indices = np.where(cls.state_relation_entities_adjacent_matrix[:, j] == val)[0].tolist()
                entity_indices_tuple = (
                    val,
                    cls.state_relations_adjacent_matrix_02[entity_indices[0], j],
                    cls.update_state_functions_dicts_02[cls.state_relations_adjacent_matrix_02[entity_indices[0], j]],
                    entity_indices,
                    j,
                )
                cls.state_entity_indices_list.append(entity_indices_tuple)

        pass  # def

    # @classmethod
    # def get_relation_of_states(cls, source_state: StateType, target_state: StateType, mode: str = 'all'):  # HACK暂时用不到
    #     """
    #     获取两个状态之间的关系。
    #
    #     Args:
    #         source_state (StateType): 源状态
    #         target_state (StateType): 目标状态
    #         mode (str, optional): 获取模式。可选值为`all`、`target`、`one`。默认为`all`，获取整个【状态关系邻接矩阵01】；`target`，获取源状态与所有汇状态之间的关系；`one`，获取两个状态之间的关系。 默认是 'all'。
    #
    #     Returns:
    #         如果`mode`为`all`，则返回整个【状态关系邻接矩阵01】；如果`mode`为`target`，则返回源状态与所有汇状态之间的关系；如果`mode`为`one`，则返回两个状态之间的关系。
    #     """
    #     if mode == 'all':  # 直接获取整个【状态关系邻接矩阵01】
    #         return cls.state_relations_adjacent_matrix_01
    #     elif mode == 'target':  # 获取源状态与所有汇状态之间的关系
    #         return cls.states_relations_indices_table[(cls.states_relations_indices_table[:, 0] == source_state), 2]
    #     elif mode == 'one':  # 获取两个状态之间的关系
    #         return cls.states_relations_indices_table[(cls.states_relations_indices_table[:, 0] == source_state) & (cls.states_relations_indices_table[:, 1] == target_state), 2]
    #     else:
    #         raise ValueError("参数`mode`的值不正确。")
    #     pass  # def

    @classmethod
    def init_list_of_relation_in_state_of_agents(cls, agent: Agent, interagent: AgentInteragent):  # HACK暂时用不到
        """
        初始化个体状态关系列表
        """
        interagent.cre = cls.calc_list_of_relation_in_state_of_agents(interagent, isState=agent.on, goal="cre")
        interagent.deb = cls.calc_list_of_relation_in_state_of_agents(interagent, isState=agent.on, goal="deb")
        pass

    @classmethod
    def calc_state_on(cls):
        """
        计算示性向量之于个体on的。
        
        Returns:
            result: 示性向量之计算后的。
            source_state_changes: 示性向量之源状态改变的。
            
        """
        result = (cls.agent.hel | cls.agent.isv | cls.agent.ilq | cls.agent.br)
        source_state_changes = (cls.agent.on != result)
        return result.squeeze(), source_state_changes.squeeze()
        pass

    @classmethod
    def calc_state_hel(cls):
        """
        计算示性向量之于个体hel的。

        Returns:
            result: 示性向量之计算后的。
            source_state_changes: 示性向量之源状态改变的。

        """
        result = ((cls.agent.E_all >= LESS1) & (cls.agent.A_Q >= LESS1) & (cls.agent.Shock_def_t + LESS1 <= cls.agent.E_all) & (cls.agent.Shock_run_t + LESS1 <= cls.agent.A_Q) & (cls.agent.on))
        source_state_changes = (cls.agent.hel != result)
        return result.squeeze(), source_state_changes.squeeze()
        pass

    @classmethod
    def calc_state_isv(cls):
        """
        计算示性向量之于个体isv的。

        Returns:
            result: 示性向量之计算后的。
            source_state_changes: 示性向量之源状态改变的。

        """
        result = (((cls.agent.A_all < cls.agent.Z_all + LESS1) | (cls.agent.E_all < LESS1) | (cls.agent.Shock_def_t + LESS1 > cls.agent.E_all)) & cls.agent.on)
        source_state_changes = (cls.agent.isv != result)
        return result.squeeze(), source_state_changes.squeeze()
        pass

    @classmethod
    def calc_state_ilq(cls):
        """
        计算示性向量之于个体ilq的。

        Returns:
            result: 示性向量之计算后的。
            source_state_changes: 示性向量之源状态改变的。

        """
        result = (((cls.agent.A_Q < LESS1) | (cls.agent.Shock_run_t + LESS1 > cls.agent.A_Q)) & cls.agent.on)
        source_state_changes = (cls.agent.ilq != result)
        return result.squeeze(), source_state_changes.squeeze()
        pass

    @classmethod
    def calc_state_br(cls):
        """
        计算示性向量之于个体br的。

        Returns:
            result: 示性向量之计算后的。
            source_state_changes: 示性向量之源状态改变的。

        """
        result = (cls.agent.isv | cls.agent.ilq)  # TODO 这个仅仅是目前基准算法简化的做法
        source_state_changes = (cls.agent.br != result)
        return result.squeeze(), source_state_changes.squeeze()
        pass

    @classmethod
    def calc_state_off(cls):
        """
        计算示性向量之于个体off的。

        Returns:
            result: 示性向量之计算后的。
            source_state_changes: 示性向量之源状态改变的。

        """
        result = cls.agent.br | cls.agent.off
        source_state_changes = (cls.agent.off != result)
        return result.squeeze(), source_state_changes.squeeze()
        pass


    @classmethod
    def update_state_if_equity(cls, source_state: StateType, source_state_changes: StateType, target_state: StateType):
        """
        当关系是【同】的时候，更新

        Args:
            source_state (StateType): 源状态
            source_state_changes (StateType): 源状态的变动示性向量
            target_state (StateType): 目标状态

        Returns:
            target_state (StateType): 计算后的目标状态

        """
        # target_state[source_state_changes] = source_state[source_state_changes]
        return target_state
        pass  # def

    @classmethod
    def update_state_if_handle(cls, source_state: StateType, source_state_changes: StateType, target_state: StateType):
        """
        当关系是【手】的时候，更新

        Args:
            source_state (StateType): 源状态
            source_state_changes (StateType): 源状态的变动示性向量
            target_state (StateType): 目标状态

        Returns:
            target_state (StateType): 计算后的目标状态

        """
        # target_state[source_state_changes] = source_state[source_state_changes]
        return target_state
        pass  # def

    @classmethod
    def update_state_if_none(cls, source_state: StateType, source_state_changes: StateType, target_state: StateType):
        """
        当关系是【无】的时候，更新

        Args:
            source_state (StateType): 源状态
            source_state_changes (StateType): 源状态的变动示性向量
            target_state (StateType): 目标状态

        Returns:
            target_state (StateType): 计算后的目标状态

        """
        # target_state[source_state_changes] = source_state[source_state_changes]
        return target_state
        pass  # def

    @classmethod
    def update_state_if_uncertain(cls, source_state: StateType, source_state_changes: StateType, target_state: StateType):
        """
        当关系是【疑】的时候，更新

        Args:
            source_state (StateType): 源状态
            source_state_changes (StateType): 源状态的变动示性向量
            target_state (StateType): 目标状态

        Returns:
            target_state (StateType): 计算后的目标状态

        """
        # target_state[source_state_changes] = source_state[source_state_changes]
        return target_state
        pass  # def

    @classmethod
    def update_state_if_parent(cls, source_state: StateType, source_state_changes: StateType, target_state: StateType):
        """
        当关系是【母】的时候，更新

        Args:
            source_state (StateType): 源状态
            source_state_changes (StateType): 源状态的变动示性向量
            target_state (StateType): 目标状态

        Returns:
            target_state (StateType): 计算后的目标状态

        """
        # target_state[source_state_changes] = source_state[source_state_changes]
        return target_state
        pass  # def

    @classmethod
    def update_state_if_child(cls, source_state: StateType, source_state_changes: StateType, target_state: StateType):
        """
        当关系是【子】的时候，更新

        Args:
            source_state (StateType): 源状态
            source_state_changes (StateType): 源状态的变动示性向量
            target_state (StateType): 目标状态

        Returns:
            target_state (StateType): 计算后的目标状态

        """

        ## NOTE：本项目不考虑【子】状态更新，以下代码段不需要用到
        # # target_state= (~target_state & source_state_changes) | (target_state & ~source_state_changes)  # NOTE和下面一行的语句实现结果是等价的，但是运算速度可能慢一点
        # is_changed_state = (target_state[source_state_changes] != source_state[source_state_changes]).any()
        # if is_changed_state:
        #     target_state[source_state_changes] = source_state[source_state_changes]
        # return target_state, target_interstate, is_changed_state

        # target_state[source_state_changes] = source_state[source_state_changes]
        return target_state
        pass  # def

    @classmethod
    def update_state_if_exclusive(cls, source_state: StateType, source_state_changes: StateType, target_state: StateType):
        """
        当关系是【斥】的时候，更新

        Args:
            source_state (StateType): 源状态
            source_state_changes (StateType): 源状态的变动示性向量
            target_state (StateType): 目标状态

        Returns:
            target_state (StateType): 计算后的目标状态

        """
        # target_state= (~target_state & source_state_changes) | (target_state & ~source_state_changes)  # NOTE和下面一行的语句实现结果是等价的，但是运算速度可能慢一点
        target_state[source_state_changes] = ~source_state[source_state_changes]
        return target_state
        pass  # def

    @classmethod
    def update_state_if_nand(cls, source_state: StateType, source_state_changes: StateType, target_state: StateType):
        """
        当关系是【非】的时候，更新

        Args:
            source_state (StateType): 源状态
            source_state_changes (StateType): 源状态的变动示性向量
            target_state (StateType): 目标状态

        Returns:
            target_state (StateType): 计算后的目标状态

        """
        # target_state= (~target_state & source_state_changes) | (target_state & ~source_state_changes)  # NOTE和下面一行的语句实现结果是等价的，但是运算速度可能慢一点
        target_state[source_state_changes] = ~source_state[source_state_changes]
        return target_state
        pass  # def

    @classmethod
    def update_target_state_if_none(cls, target_state_from_source_states: np.array):
        """
        当关系是【无】的时候，更新

        Args:
            target_state_from_source_states (np.array): 目标状态相关的各源状态

        Returns:
            target_state (StateType): 计算后的目标状态

        """
        target_state = target_state_from_source_states.all(axis=0)
        return target_state
        pass  # def

    @classmethod
    def update_target_state_if_and(cls, target_state_from_source_states: np.array):
        """
        当关系是【与】的时候，更新

        Args:
            target_state_from_source_states (np.array): 目标状态相关的各源状态

        Returns:
            target_state (StateType): 计算后的目标状态

        """
        target_state = target_state_from_source_states.all(axis=0)
        return target_state
        pass  # def

    @classmethod
    def together_isOn(cls, agent: Agent, interagent: AgentInteragent):  # HACK虽然无用，但是可以先保留
        """汇总示性向量之于个体on的。"""
        condition = (agent.hel | agent.isv | agent.ilq | agent.br)
        if (agent.on != condition).any():
            agent.on = condition
            interagent.on = (agent.on & agent.on.T)
            pass
        pass

    @classmethod
    def calc_list_of_relation_in_state_of_agents(cls, interagent: AgentInteragent, isState: StateType, goal: str):
        """
        计算信息列表之于各状态个体之各关联个体。

        参数``goal``可选项：
            - ``deb``:  计算对应的deb方个体；
            - ``cre``:  计算对应的cre方个体；

        Args:
            interagent (AgentInteragent): AgentInteragent
            isState ():
            goal (str): 参数，确定计算deb方或cre方。

        Returns: list_of_relation_in_state_of_agents

        """

        # 计算示性矩阵之于个体间风险敞口的
        if goal == "deb":
            is_exposure = ((interagent.A_IB > 0.0) & isState)
        elif goal == "cre":
            is_exposure = ((interagent.Z_IB > 0.0) & isState)
        else:
            pass
        list_of_relation_in_state_of_agents = np.array([np.array(None) for i in range(env['num_agent'])])  # BUG TODO：用None会导致整个数据类型变成object，而不是array，所以需要改成np.nan
        for i in range(env['num_agent']):
            list_of_relation_in_state_of_agents[i] = np.where(is_exposure[i, :])[0]  # 获取对应状态下的cre或者deb关系的个体列表
            pass
        return list_of_relation_in_state_of_agents
        pass

    @classmethod
    def update_states(cls, way: str = 'any'):
        """
        更新各个体之状态。

        Args:
            way (str): 参数，确定更新方式。

        参数``way``可选项：#TODO

        - ``any``:  到任意状态；
        - ``hel``:  到hel状态；
        - ``isv``:  到isv状态；
        - ``ilq``:  到ilq状态；
        - ``br``:  到br状态；
        - ``off``:  到off状态；

        Returns: None

        """

        ## 设置状态集合数据数组`states_data_array`
        states_data_array = np.asarray(cls.states_data_list).squeeze()

        ## 设置交互状态集合数据数组`interstates_data_array`
        interstates_data_array = np.asarray(cls.interstates_data_list)

        ## 指定而计算源状态；
        states_data_changes_matrix = np.full((cls.num_states, env['num_agent']), False)  # 示性矩阵之各状态数据变动情况。每列表示单个状态之各主体变量是否变动。
        is_states_data_changed_array = states_data_changes_matrix.any(axis=1)  # 示性向量之各状态数据是否已经变动。每个元素表示单个状态是否变动。
        if way == 'any':
            for i in range(cls.num_states):
                states_data_array[i, :], states_data_changes_matrix[i, :] = cls.calc_state_functions_list[i]()  # 遍历计算各状态数据变动情况
            is_states_data_changed_array = states_data_changes_matrix.any(axis=1)
        else:
            for i in range(cls.num_states):
                states_data_array[i, :], states_data_changes_matrix[i, :] = cls.calc_state_functions_list[i]()  # 遍历计算各状态数据变动情况
            is_states_data_changed_array = states_data_changes_matrix.any(axis=1)
            pass  # if

        ## 计算交互状态
        for i in range(cls.num_states):
            interstates_data_array[i] = (np.expand_dims(states_data_array[i], axis=1) & np.expand_dims(states_data_array[i], axis=0))

        ## 数据赋值回原来的各主体
        for i in range(cls.num_states):
            cls.states_data_list[i][:] = np.expand_dims(states_data_array[i, :], axis=1)
            cls.interstates_data_list[i] = interstates_data_array[i].copy()

        ## 更新个体间interagent之各状态下之信息列表之于各个体之cre方与deb方之个体编号。#FIXME
        cls.interagent.cre_isv = cls.calc_list_of_relation_in_state_of_agents(cls.interagent, isState=cls.agent.isv, goal="cre")
        cls.interagent.deb_isv = cls.calc_list_of_relation_in_state_of_agents(cls.interagent, isState=cls.agent.isv, goal="deb")
        cls.interagent.cre_ilq = cls.calc_list_of_relation_in_state_of_agents(cls.interagent, isState=cls.agent.ilq, goal="cre")
        cls.interagent.deb_ilq = cls.calc_list_of_relation_in_state_of_agents(cls.interagent, isState=cls.agent.ilq, goal="deb")
        cls.interagent.cre_br = cls.calc_list_of_relation_in_state_of_agents(cls.interagent, isState=cls.agent.br, goal="cre")
        cls.interagent.deb_br = cls.calc_list_of_relation_in_state_of_agents(cls.interagent, isState=cls.agent.br, goal="deb")

        pass  # def

    pass  # class
