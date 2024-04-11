from py2neo import Graph
import random

class AnswerSearcher:
    def __init__(self):
        self.g = Graph("bolt://localhost:7687", auth=("neo4j", "qzx123456"))
        self.num_limit = 100
        self.templates_contain = [
            '{0}包含了以下子概念/领域:{1}',
            '{0}这个概念/领域涵盖了以下内容:{1}',
            '在{0}之下有以下几个子领域/子概念:{1}',
            '{0}这个概念/领域包括如下几个方面:{1}',
            '根据知识图谱,{0}包含以下几个部分:{1}'
        ]
        self.templates_equal = [
            '与{0}等价的一些概念有以下这些:{1}',
            '以下是和{0}等同的一些概念:{1}',
            '{0}相当于或同义于以下概念:{1}',
            '和{0}意思相同或者是等价关系的概念有:{1}',
            '{0}这个概念在知识图谱中等价于以下概念:{1}'
        ]
        self.templates_derive = [
            '{0}的来源/起源是:{1}',
            '{0}这个概念/领域源自于:{1}',
            '根据知识图谱,{0}的渊源可以追溯到:{1}',
            '{0}的起因/根源在于:{1}',
            '关于{0}的起源/由来,知识图谱显示是:{1}'
        ]
        self.templates_belong = [
            '{0}属于以下几个大类/总概念:{1}',
            '{0}这个概念/领域隶属于:{1}',
            '根据知识图谱,{0}属于以下几个上位概念:{1}',
            '{0}可以被划分到以下几个大的范畴中:{1}',
            '关于{0}的分类/所属,知识图谱显示是:{1}'
        ]
        self.templates_compose = [
            '{0}由以下几个部分/要素组成:{1}',
            '{0}这个概念/领域包括以下几个组成部分:{1}',
            '根据知识图谱,{0}是由下列几个部分构成的:{1}',
            '{0}可以分解为以下几个组成单元:{1}',
            '关于{0}的组成结构,知识图谱显示包括:{1}'
        ]
        self.templates_engname = [
            '根据知识图谱,{0}的英文名是:{1}',
            '{0}这一概念在英文中被称为:{1}',
            '关于{0}的英文称呼,知识图谱给出的是:{1}',
            '{0}对应的英文名称是:{1}',
            '在英语表达中,{0}通常被译为:{1}'
        ]
        self.templates_realize = [
            '实现{0}的主要手段/方式有:{1}',
            '根据知识图谱,{0}可以通过以下几种方式来实现:{1}',
            '{0}这个目标/任务的实现途径包括:{1}',
            '关于如何实现{0},知识图谱给出的方法有:{1}',
            '{0}可以采取以下几种具体措施来完成:{1}'
        ]
        self.templates_define = [
            '{0}被定义/描述为:{1}',
            '根据知识图谱,{0}这个概念的定义是:{1}',
            '{0}的含义/内涵可以概括为:{1}',
            '关于{0}的定义,知识图谱给出的解释是:{1}',
            '{0}这个术语在知识图谱中被解释为:{1}'
        ]
        self.templates_target = [
            '{0}的主要目的是:{1}',
            '关于{0}这个概念/领域的目标有:{1}',
            '{0}所要达到的目的包括以下几个方面:{1}',
            '根据知识图谱,{0}的存在目的是:{1}',
            '{0}这个行为/举措的终极目标是:{1}'
        ]
        self.templates_content = [
            '{0}的主要作用/功能是:{1}',
            '根据知识图谱,{0}发挥的作用有:{1}',
            '{0}所起到的关键作用包括:{1}',
            '关于{0}的作用,知识图谱给出了以下几点:{1}',
            '{0}在...中起到了以下几个方面的作用:{1}'
        ]
        self.templates_effect = [
            '{0}的主要作用包括:{1}'
        ]
        self.templates_character = [
            '{0}的主要特点/特征有:{1}',
            '根据知识图谱,{0}具有以下几个特点:{1}',
            '{0}所呈现出的一些关键特征包括:{1}',
            '关于{0}的特点,知识图谱总结为:{1}',
            '从一些方面来看,{0}表现出了以下几个方面的特点:{1}'
        ]
        self.templates_method = [
            '{0}可采用的主要方法/途径有:{1}',
            '根据知识图谱,实现{0}的常见方法包括:{1}',
            '{0}这一目标/任务可以通过以下几种方式来完成:{1}',
            '关于如何{0},知识图谱给出的方法有:{1}',
            '{0}可以考虑使用以下几种方法:{1}'
        ]
        self.templates_flaw = [
            '{0}的主要缺点/不足之处有:{1}',
            '根据知识图谱,{0}存在以下几个缺陷:{1}',
            '{0}这种做法/方式的一些问题或局限性包括:{1}',
            '关于{0}的缺点,知识图谱指出了以下几点:{1}',
            '从某些角度来看,{0}仍然存在下列几个不足:{1}'
        ]
        self.templates_create_time = [
            '{0}创建于{1}',
            '根据知识图谱,{0}的创建时间是{1}',
            '{0}这个概念/事物产生于{1}',
            '关于{0}的创建时间,知识图谱记录的是{1}',
            '{0}可追溯到{1}时期'
        ]
        self.templates_creator = [
            '根据知识图谱,{0}的创始人或机构是{1}',
            '{0}是由{1}所创立的'
        ]
        self.templates_link = [
            '如果你想了解更多关于{0}的信息,可以访问这些网页链接:{1}',
            '{0}相关的一些网页链接有:{1}',
            '根据知识图谱,与{0}有关的推荐网页链接包括:{1}',
            '关于{0}这个主题,以下网页链接或许会有所帮助:{1}',
            '你可以通过查看这些网页链接,来加深对{0}的理解:{1}'
        ]
        self.templates_exercise = [
            '关于{0}这一主题,一些相关习题有:{1}',
            '{0}方面的习题包括:{1}',
            '根据知识图谱,与{0}相关的习题有:{1}',
            '如果你想巩固{0}方面的知识,可以尝试做以下习题:{1}',
            '为了加深对{0}的理解,这些习题或许有帮助:{1}'
        ]

    '''执行cypher查询，并返回相应结果'''
    def search_main(self, sqls):
        final_answers = []
        for sql_ in sqls:
            question_type = sql_['question_type']
            queries = sql_['sql']
            answers = []
            for query in queries:
                ress = self.g.run(query).data()
                answers += ress
            final_answer = self.answer_prettify(question_type, answers)
            final_answers.append(final_answer)
        return final_answers

    '''根据对应的qustion_type，调用相应的回复模板'''
    def answer_prettify(self, question_type, answers):
        final_answer = []
        if not answers:
            return ''
        if question_type == 'contain':
            desc = [i['n.name'] for i in answers]  # 假设包含概念在'n.name'字段
            subject = answers[0]['m.name']
            if all(x is None for x in desc) and len(desc) > 0:
                final_answer = '在我们知识图谱里找到的答案就这么多'.format(subject)
            else:
                filtered_desc = [d for d in desc if d is not None] # 过滤掉None值
                random_template = random.choice(self.templates_contain)
                final_answer = random_template.format(subject, ';'.join(filtered_desc)[:self.num_limit])

        elif question_type == 'equal':
            desc = [i['n.name'] for i in answers]  
            subject = answers[0]['m.name']
            if all(x is None for x in desc) and len(desc) > 0:
                final_answer = '在我们知识图谱里找到的答案就这么多'.format(subject)
            else:
                filtered_desc = [d for d in desc if d is not None] # 过滤掉None值
                random_template = random.choice(self.templates_equal)
                final_answer = random_template.format(subject, ';'.join(filtered_desc)[:self.num_limit])

        elif question_type == 'exercise':
            desc = [i['n.name'] for i in answers]  
            subject = answers[0]['m.name']
            if all(x is None for x in desc) and len(desc) > 0:
                final_answer = '在我们知识图谱里找到的答案就这么多'.format(subject)
            else:
                filtered_desc = [d for d in desc if d is not None] # 过滤掉None值
                random_template = random.choice(self.templates_exercise)
                final_answer = random_template.format(subject, ';'.join(filtered_desc)[:self.num_limit])

        elif question_type == 'derive':
            desc = [i['n.name'] for i in answers]  
            subject = answers[0]['m.name']
            if all(x is None for x in desc) and len(desc) > 0:
                final_answer = '在我们知识图谱里找到的答案就这么多'.format(subject)
            else:
                filtered_desc = [d for d in desc if d is not None] # 过滤掉None值
                random_template = random.choice(self.templates_derive)
                final_answer = random_template.format(subject, ';'.join(filtered_desc)[:self.num_limit])

        elif question_type == 'belong':
            desc = [i['n.name'] for i in answers]  
            subject = answers[0]['m.name']
            if all(x is None for x in desc) and len(desc) > 0:
                final_answer = '在我们知识图谱里找到的答案就这么多'.format(subject)
            else:
                filtered_desc = [d for d in desc if d is not None] # 过滤掉None值
                random_template = random.choice(self.templates_belong)
                final_answer = random_template.format(subject, ';'.join(filtered_desc)[:self.num_limit])

        elif question_type == 'compose':
            desc = [i['n.name'] for i in answers]  
            subject = answers[0]['m.name']
            if all(x is None for x in desc) and len(desc) > 0:
                final_answer = '在我们知识图谱里找到的答案就这么多'.format(subject)
            else:
                filtered_desc = [d for d in desc if d is not None] # 过滤掉None值
                random_template = random.choice(self.templates_compose)
                final_answer = random_template.format(subject, ';'.join(filtered_desc)[:self.num_limit])

        elif question_type == 'engname':
            desc = [i['m.英文名'] for i in answers]  
            subject = answers[0]['m.name']
            if all(x is None for x in desc) and len(desc) > 0:
                final_answer = '在我们知识图谱里找到的答案就这么多'.format(subject)
            else:
                filtered_desc = [d for d in desc if d is not None] # 过滤掉None值
                random_template = random.choice(self.templates_engname)
                final_answer = random_template.format(subject, ';'.join(filtered_desc)[:self.num_limit])

        elif question_type == 'realize':
            desc = [i['n.name'] for i in answers]  
            subject = answers[0]['m.name']
            if all(x is None for x in desc) and len(desc) > 0:
                final_answer = '在我们知识图谱里找到的答案就这么多'.format(subject)
            else:
                filtered_desc = [d for d in desc if d is not None] # 过滤掉None值
                random_template = random.choice(self.templates_realize)
                final_answer = random_template.format(subject, ';'.join(filtered_desc)[:self.num_limit])

        elif question_type == 'define':
            desc = [i['m.被定义为'] for i in answers]  
            subject = answers[0]['m.name']
            if all(x is None for x in desc) and len(desc) > 0:
                final_answer = '在我们知识图谱里找到的答案就这么多'.format(subject)
            else:
                filtered_desc = [d for d in desc if d is not None] # 过滤掉None值
                random_template = random.choice(self.templates_define)
                final_answer = random_template.format(subject, ';'.join(filtered_desc)[:self.num_limit])

        elif question_type == 'content':
            desc = [i['m.内容'] for i in answers]  
            subject = answers[0]['m.name']
            if all(x is None for x in desc) and len(desc) > 0:
                final_answer = '在我们知识图谱里找到的答案就这么多'.format(subject)
            else:
                filtered_desc = [d for d in desc if d is not None] # 过滤掉None值
                random_template = random.choice(self.templates_content)
                final_answer = random_template.format(subject, ';'.join(filtered_desc)[:self.num_limit])

        elif question_type == 'target':
            desc = [i['m.目标'] for i in answers]  
            subject = answers[0]['m.name']
            if all(x is None for x in desc) and len(desc) > 0:
                final_answer = '在我们知识图谱里找到的答案就这么多'.format(subject)
            else:
                filtered_desc = [d for d in desc if d is not None] # 过滤掉None值
                random_template = random.choice(self.templates_target)
                final_answer = random_template.format(subject, ';'.join(filtered_desc)[:self.num_limit])
        
        elif question_type == 'effect':
            desc = [i['m.作用'] for i in answers]
            subject = answers[0]['m.name']
            if all(x is None for x in desc) and len(desc) > 0:
                final_answer = '在我们知识图谱里找到的答案就这么多'.format(subject)
            else:
                filtered_desc = [d for d in desc if d is not None] # 过滤掉None值
                random_template = random.choice(self.templates_effect)
                final_answer = random_template.format(subject, ';'.join(filtered_desc)[:self.num_limit])

        elif question_type == 'character':
            desc = [i['m.特点'] for i in answers]
            subject = answers[0]['m.name']
            if all(x is None for x in desc) and len(desc) > 0:
                final_answer = '在我们知识图谱里找到的答案就这么多'.format(subject)
            else:
                filtered_desc = [d for d in desc if d is not None] # 过滤掉None值
                random_template = random.choice(self.templates_character)
                final_answer = random_template.format(subject, ';'.join(filtered_desc)[:self.num_limit])

        elif question_type == 'method':
            desc = [i['m.方法'] for i in answers]
            subject = answers[0]['m.name']
            if all(x is None for x in desc) and len(desc) > 0:
                final_answer = '在我们知识图谱里找到的答案就这么多'.format(subject)
            else:
                filtered_desc = [d for d in desc if d is not None] # 过滤掉None值
                random_template = random.choice(self.templates_method)
                final_answer = random_template.format(subject, ';'.join(filtered_desc)[:self.num_limit])

        elif question_type == 'flaw':
            desc = [i['m.缺点'] for i in answers]
            subject = answers[0]['m.name']
            if all(x is None for x in desc) and len(desc) > 0:
                final_answer = '在我们知识图谱里找到的答案就这么多'.format(subject)
            else:
                filtered_desc = [d for d in desc if d is not None] # 过滤掉None值
                random_template = random.choice(self.templates_flaw)
                final_answer = random_template.format(subject, ';'.join(filtered_desc)[:self.num_limit])

        elif question_type == 'create_time':
            desc = [i['m.创建时间'] for i in answers]
            subject = answers[0]['m.name']
            if all(x is None for x in desc) and len(desc) > 0:
                final_answer = '在我们知识图谱里找到的答案就这么多'.format(subject)
            else:
                filtered_desc = [d for d in desc if d is not None] # 过滤掉None值
                random_template = random.choice(self.templates_create_time)
                final_answer = random_template.format(subject, ';'.join(filtered_desc)[:self.num_limit])

        elif question_type == 'creator':
            desc = [i['m.创建者'] for i in answers]
            subject = answers[0]['m.name']
            if all(x is None for x in desc) and len(desc) > 0:
                final_answer = '在我们知识图谱里找到的答案就这么多'.format(subject)
            else:
                filtered_desc = [d for d in desc if d is not None] # 过滤掉None值
                random_template = random.choice(self.templates_creator)
                final_answer = random_template.format(subject, ';'.join(filtered_desc)[:self.num_limit])

        elif question_type == 'link':
            desc = [i['m.链接'] for i in answers]  
            subject = answers[0]['m.name']
            if all(x is None for x in desc) and len(desc) > 0:
                final_answer = '在我们知识图谱里找到的答案就这么多'
            else:
                filtered_desc = [d for d in desc if d is not None] # 过滤掉None值
                random_template = random.choice(self.templates_link)
                final_answer = random_template.format(subject, ';'.join(filtered_desc)[:self.num_limit]) 

        return final_answer


if __name__ == '__main__':
    searcher = AnswerSearcher()