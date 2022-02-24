import numpy
import numpy as np


def levenshtein_distance(hypothesis, reference):
    """
    计算 Levenshtein 距离
    C: correct
    W: wrong
    I: insert
    D: delete
    S: substitution
    :param hypothesis: 推测的 我要去吃晚饭了
    :param reference: 真实的 她马上要去吃午饭
    :return:
    """
    hypothesis = list(hypothesis)
    reference = list(reference)
    len_hyp = len(hypothesis)
    len_ref = len(reference)
    cost_matrix = np.zeros((len_hyp + 1, len_ref + 1), dtype=np.int16)

    ops_matrix = np.zeros((len_hyp + 1, len_ref + 1), dtype=np.int8)

    for i in range(len_hyp + 1):
        cost_matrix[i][0] = i
    for j in range(len_ref + 1):
        cost_matrix[0][j] = j

    for i in range(1, len_hyp + 1):
        for j in range(1, len_ref + 1):
            if hypothesis[i - 1] == reference[j - 1]:
                cost_matrix[i][j] = cost_matrix[i - 1][j - 1]
            else:
                substitution = cost_matrix[i - 1][j - 1] + 1
                insertion = cost_matrix[i - 1][j] + 1
                deletion = cost_matrix[i][j - 1] + 1

                compare_val = [substitution, insertion, deletion]  # 优先级

                min_val = min(compare_val)
                operation_idx = compare_val.index(min_val) + 1
                cost_matrix[i][j] = min_val
                ops_matrix[i][j] = operation_idx

    # 保存对齐的元素下标
    match_idx = []
    i = len_hyp
    j = len_ref
    nb_map = {"N": len_ref, "C": 0, "W": 0, "I": 0, "D": 0, "S": 0}
    while i >= 0 or j >= 0:
        i_idx = max(0, i)
        j_idx = max(0, j)

        if ops_matrix[i_idx][j_idx] == 0:
            if i - 1 >= 0 and j - 1 >= 0:
                match_idx.append((j - 1, i - 1))
                nb_map['C'] += 1

            i -= 1
            j -= 1
        elif ops_matrix[i_idx][j_idx] == 2:  # insert
            i -= 1
            nb_map['I'] += 1
        elif ops_matrix[i_idx][j_idx] == 3:  # delete
            j -= 1
            nb_map['D'] += 1
        elif ops_matrix[i_idx][j_idx] == 1:  # substitute
            i -= 1
            j -= 1
            nb_map['S'] += 1

        if i < 0 and j >= 0:
            nb_map['D'] += 1
        elif j < 0 and i >= 0:
            nb_map['I'] += 1

    match_idx.reverse()
    wrong_cnt = cost_matrix[len_hyp][len_ref]
    nb_map["W"] = wrong_cnt
    return nb_map['W'], nb_map['N']


def cer(r, h):
    """
    计算 CER
    :param r: 真实的 她马上要去吃午饭
    :param h: 推测的 我要去吃晚饭了
    :return:
    """
    return levenshtein_distance(h, r)


def wer(r, h):
    """
    计算 WER
    :param r: 真实的 I am going to eat lunch
    :param h: 预测的 She is going to eat supper
    :return:
    """
    r = r.split()
    h = h.split()
    d = numpy.zeros((len(r) + 1) * (len(h) + 1), dtype=numpy.uint8)
    d = d.reshape((len(r) + 1, len(h) + 1))
    for i in range(len(r) + 1):
        for j in range(len(h) + 1):
            if i == 0:
                d[0][j] = j
            elif j == 0:
                d[i][0] = i

    for i in range(1, len(r) + 1):
        for j in range(1, len(h) + 1):
            if r[i - 1] == h[j - 1]:
                d[i][j] = d[i - 1][j - 1]
            else:
                substitution = d[i - 1][j - 1] + 1
                insertion = d[i][j - 1] + 1
                deletion = d[i - 1][j] + 1
                d[i][j] = min(substitution, insertion, deletion)

    return d[len(r)][len(h)], len(r)


if __name__ == '__main__':
    print(wer("I am going to eat lunch", "She's going to eat supper"))
    print(cer("我要去吃晚饭了", "她马上要去吃午饭"))
