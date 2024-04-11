import os
import ahocorasick

class QuestionClassifier:
    def __init__(self):
        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        #　特征词路径
        self.human_lab_path = os.path.join(cur_dir, 'dict/人物_实验室.txt')
        self.time_path = os.path.join(cur_dir, 'dict/时间.txt')
        self.text_path = os.path.join(cur_dir, 'dict/文本.txt')
        self.link_path = os.path.join(cur_dir, 'dict/链接.txt')
        self.semantic_search_path = os.path.join(cur_dir, 'dict/语义搜索.txt')
        self.knowledge_representation_path = os.path.join(cur_dir, 'dict/知识表示.txt')
        self.knowledge_extract_path = os.path.join(cur_dir, 'dict/知识抽取.txt')
        self.knowledge_storage_path = os.path.join(cur_dir, 'dict/知识存储.txt')
        self.knowledge_engineer_path = os.path.join(cur_dir, 'dict/知识工程.txt')
        self.knowledge_incorporate_path = os.path.join(cur_dir, 'dict/知识融合.txt')
        self.knowledge_graph_path = os.path.join(cur_dir, 'dict/知识图谱.txt')
        self.knowledge_graph_project_path = os.path.join(cur_dir, 'dict/知识图谱项目.txt')
        self.knowledge_deduce_path = os.path.join(cur_dir, 'dict/知识推理.txt')
        self.knowledge_qa_path = os.path.join(cur_dir, 'dict/知识问答.txt')
        self.deny_path = os.path.join(cur_dir, 'dict/deny.txt')
        # 加载特征词
        self.human_lab_wds= [i.strip() for i in open(self.human_lab_path, encoding='utf-8') if i.strip()]
        self.time_wds= [i.strip() for i in open(self.time_path, encoding='utf-8') if i.strip()]
        self.text_wds= [i.strip() for i in open(self.text_path, encoding='utf-8') if i.strip()]
        self.link_wds= [i.strip() for i in open(self.link_path, encoding='utf-8') if i.strip()]
        self.semantic_search_wds= [i.strip() for i in open(self.semantic_search_path, encoding='utf-8') if i.strip()]
        self.knowledge_representation_wds= [i.strip() for i in open(self.knowledge_representation_path, encoding='utf-8') if i.strip()]
        self.knowledge_extract_wds= [i.strip() for i in open(self.knowledge_extract_path, encoding='utf-8') if i.strip()]
        self.knowledge_storage_wds= [i.strip() for i in open(self.knowledge_storage_path, encoding='utf-8') if i.strip()]
        self.knowledge_engineer_wds= [i.strip() for i in open(self.knowledge_engineer_path, encoding='utf-8') if i.strip()]
        self.knowledge_incorporate_wds= [i.strip() for i in open(self.knowledge_incorporate_path, encoding='utf-8') if i.strip()]
        self.knowledge_graph_wds= [i.strip() for i in open(self.knowledge_graph_path, encoding='utf-8') if i.strip()]
        self.knowledge_graph_project_wds= [i.strip() for i in open(self.knowledge_graph_project_path, encoding='utf-8') if i.strip()]
        self.knowledge_deduce_wds= [i.strip() for i in open(self.knowledge_deduce_path, encoding='utf-8') if i.strip()]
        self.knowledge_qa_wds= [i.strip() for i in open(self.knowledge_qa_path, encoding='utf-8') if i.strip()]
        self.region_words = set(self.semantic_search_wds + self.knowledge_representation_wds + self.knowledge_extract_wds +
                                self.knowledge_storage_wds + self.knowledge_engineer_wds + self.knowledge_incorporate_wds + 
                                self.knowledge_graph_wds + self.knowledge_graph_project_wds + self.knowledge_deduce_wds +
                                self.knowledge_qa_wds)
        self.deny_words = [i.strip() for i in open(self.deny_path, encoding='utf-8') if i.strip()]
        # 构造领域actree
        self.region_tree = self.build_actree(list(self.region_words))
        # 构建词典
        self.wdtype_dict = self.build_wdtype_dict()
        # 问句疑问词
        self.contain_qwds = ['包含', '包括', '涉及', '涵盖', '其中一个', '有哪些方面', '有几个', '含有', '子概念', '有几类', '类别']
        self.equal_qwds = ['等于', '相当于', '相同', '一致', '相同的意思', '等价', '同义', '一回事', '对等', '等同', '同一个', '又称', '别名']
        self.derive_qwds = ['来自', '体现', '基础', '源于', '起源', '产生', '衍生', '根源', '由来', '来源']
        self.belong_qwds = ['归类', '属于', '所属', '从属', '隶属于', '归属']
        self.realize_qwds = ['方法', '采用', '使用', '通过', '基于', '解决', '核心', '关键', '设计', '构建', '实施', '实行', '优化'
                            , '部署', '开发', '验证', '探索', '整合', '调研', '调查', '规划', '迭代', '策略',
                            '完成', '达成', '实现', '实行', '用了什么技术', '技术要点', '手段']
        self.compose_qwds = ['成分', '元素', '组合', '组成', '要素', '构成', '形成', '构筑', '组织']
        self.exercise_qwds = ['习题', '题目', '练习', '训练', '点题', '做题']

        self.define_qwds = ['定义', '是什么意思', '是什么东西', '是指什么', '什么是', '意思', '含义', '是啥意思', '是啥东西', '是指啥', '啥是', '即什么', 
                            '解释', '啥叫','内容', '详细信息', '描述']
        self.engname_qwds = ['英文名', '用英语怎么说', '译名', '英文缩写', '英文简称', '英文称谓', '英文名称']
        self.target_qwds = ['目标', '目的', '意图', '预期', '旨在', '致力于', '是为了']
        self.content_qwds = ['定义', '是什么意思', '是什么东西', '是指什么', '什么是', '意思', '含义', '是啥意思', '是啥东西', '是指啥', '啥是', '即什么', 
                            '解释', '啥叫','内容', '详细信息', '描述']
        self.effect_qwds = ['影响', '作用', '能做什么', '有什么用', '有啥用', '功能', '用途', '效果', '可以干什么', '是干什么的', '干啥']
        self.character_qwds = ['特点', '针对', '解决了', '特色', '支持', '优点', '特征', '优势', '独特', '强项', '性质', '长处', '好处']
        self.method_qwds = ['方法', '采用', '使用', '通过', '基于', '解决', '核心', '关键', '设计', '构建', '实施', '实行', '优化'
                            , '部署', '开发', '验证', '探索', '整合', '调研', '调查', '规划', '迭代', '策略',
                            '完成', '达成', '实现', '实行', '用了什么技术', '技术要点', '手段']
        self.flaw_qwds = ['问题', '缺点', '但需要', '需要花费', '无法', '太弱', '缺少', '低下', '耗费', '差', '不高', '耗时', '费力', '代价', 
                          '弊端', '局限', '难题', '不足', '限制', '风险', '缺乏', '效率低', '不可靠', '复杂', '易错', '成本高', '不适用', '依赖性', '开销']
        self.create_time_qwds = ['年', '月', '时间', '日期', '创建时间', '几号', '天', '时候', '多久', '好久', '天数']
        self.creator_qwds = ['专家', '大学', '实验室', '公司', '创始人', '研究院', '研究所', '基金会', '工程师', '学者', '学家', '等人', '提出', '研究计划局',
                              '会议', '组织', '发起', '领导', '建立', '创建', '研究者', '带领', '创建', '创办', '成立了', '导师', '谁']
        self.link_qwds = ['链接', '网址', '更多信息']


        print('model init finished ......')

        return

    '''分类主函数'''
    def classify(self, question):
        data = {}
        knowledge_dict = self.check_term(question)
        if not knowledge_dict:
            return {}
        data['args'] = knowledge_dict
        #收集问句当中所涉及到的实体类型
        types = []
        for type_ in knowledge_dict.values():
            types += type_
        question_type = 'others'

        question_types = []

        # 实体之间的包含关系查询
        if self.check_words(self.contain_qwds, question):
            question_type = 'contain'
            question_types.append(question_type)

        # 实体之间的等价关系查询
        if self.check_words(self.equal_qwds, question):
            question_type = 'equal'
            question_types.append(question_type)

        # 实体之间的来源关系查询
        if self.check_words(self.derive_qwds, question):
            question_type = 'derive'
            question_types.append(question_type)
        
        # 实体之间的属于关系查询
        if self.check_words(self.belong_qwds, question):
            question_type = 'belong'
            question_types.append(question_type)
        
        # 实体之间的由组成关系查询
        if self.check_words(self.compose_qwds, question):
            question_type = 'compose'
            question_types.append(question_type)
        
        # 实体之间的习题关系查询
        if self.check_words(self.exercise_qwds, question):
            question_type = 'exercise'
            question_types.append(question_type)
        
        # 实体之间的实现关系查询
        if self.check_words(self.realize_qwds, question):
            question_type = 'realize'
            question_types.append(question_type)

        # 实体属性的被定义为关系查询
        if self.check_words(self.define_qwds, question):
            question_type = 'define'
            question_types.append(question_type)

        # 实体属性的内容关系查询
        if self.check_words(self.content_qwds, question):
            question_type = 'content'
            question_types.append(question_type)

        # 实体属性的英文名关系查询
        if self.check_words(self.engname_qwds, question):
            question_type = 'engname'
            question_types.append(question_type)
        
        # 实体属性的目标关系查询
        if self.check_words(self.target_qwds, question):
            question_type = 'target'
            question_types.append(question_type)

        # 实体属性的作用关系查询
        if self.check_words(self.effect_qwds, question):
            question_type = 'effect'
            question_types.append(question_type)

        # 实体属性的特点查询
        if self.check_words(self.character_qwds, question):
            question_type = 'character'
            question_types.append(question_type)

        # 实体属性的方法查询
        if self.check_words(self.method_qwds, question):
            question_type = 'method'
            question_types.append(question_type)

        # 实体属性的缺点查询
        if self.check_words(self.flaw_qwds, question):
            question_type = 'flaw'
            question_types.append(question_type)

        # 实体属性的创建时间查询
        if self.check_words(self.create_time_qwds, question):
            question_type = 'create_time'
            question_types.append(question_type)
            print('ok')

        # 实体属性的创建者关系查询
        if self.check_words(self.creator_qwds, question):
            question_type = 'creator'
            question_types.append(question_type)
    
        # 实体的链接属性查询
        if self.check_words(self.link_qwds, question):
            question_type = 'link'
            question_types.append(question_type)
        
        # 若没有查到相关的外部查询信息，那么则将提问者提及的术语的描述信息返回，并另请他用一种问法提问
        if question_types == []:
            question_types = ['term_desc']

        # 将多个分类结果进行合并处理，组装成一个字典
        data['question_types'] = question_types

        return data

    '''构造词对应的类型'''
    def build_wdtype_dict(self):
        wd_dict = dict()
        for wd in self.region_words:
            wd_dict[wd] = []
            if wd in self.semantic_search_wds:
                wd_dict[wd].append('semantic_search')
            if wd in self.knowledge_representation_wds:
                wd_dict[wd].append('knowledge_representation')
            if wd in self.knowledge_extract_wds:
                wd_dict[wd].append('knowledge_extract')
            if wd in self.knowledge_storage_wds:
                wd_dict[wd].append('knowledge_storage')
            if wd in self.knowledge_engineer_wds:
                wd_dict[wd].append('knowledge_engineer')
            if wd in self.knowledge_incorporate_wds:
                wd_dict[wd].append('knowledge_incorporate')
            if wd in self.knowledge_graph_wds:
                wd_dict[wd].append('knowledge_graph')
            if wd in self.knowledge_graph_project_wds:
                wd_dict[wd].append('knowledge_graph_project')
            if wd in self.knowledge_deduce_wds:
                wd_dict[wd].append('knowledge_deduce')
            if wd in self.knowledge_qa_wds:
                wd_dict[wd].append('knowledge_qa')
        return wd_dict

    '''构造actree，加速过滤'''
    def build_actree(self, wordlist):
        actree = ahocorasick.Automaton()
        for index, word in enumerate(wordlist):
            actree.add_word(word, (index, word))
        actree.make_automaton()
        return actree

    '''问句过滤'''
    def check_term(self, question):
        region_wds = []
        for i in self.region_tree.iter(question):
            wd = i[1][1]
            region_wds.append(wd)
        stop_wds = []
        for wd1 in region_wds:
            for wd2 in region_wds:
                if wd1 in wd2 and wd1 != wd2:
                    stop_wds.append(wd1)
        final_wds = [i for i in region_wds if i not in stop_wds]
        final_dict = {i:self.wdtype_dict.get(i) for i in final_wds}

        return final_dict

    '''基于特征词进行分类'''
    def check_words(self, wds, sent):
        for wd in wds:
            if wd in sent:
                return True
        return False


if __name__ == '__main__':
    handler = QuestionClassifier()
    while 1:
        question = input('input an question:')
        data = handler.classify(question)
        print(data)