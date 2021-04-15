# The tagger.py starter code for CSC384 A4.
# Currently reads in the names of the training files, test file and output file,
# and calls the tagger (which you need to implement)
import os
import sys
import numpy as np


def tag(training_list, test_file, output_file):
# def tag():
    # Tag the words from the untagged input file and write them into the output file.
    # Doesn't do much else beyond that yet.
    # training_list = ['training3.txt', 'training9.txt', 'training5.txt']
    # test_file = 'test7.txt'
    # output_file = 'autooutput.txt'
    print("Tagging the file.")
    filedata = []
    testData = []
    tag_t_1 = {'initial': 0}
    tag_t = {}
    trans_mat = {'initial': {}}
    emi_mat = {}
    for filename in training_list:
        with open(filename, "r") as f:
            for line in f.readlines():
                filedata.append((line.split()[0], line.split()[2]))
                if line.split()[2] not in tag_t:
                    tag_t[line.split()[2]] = 1
                else:
                    tag_t[line.split()[2]] += 1
                if line.split()[0] in ['.', '!', '?', '"']:
                    tag_t_1['initial'] += 1
                elif line.split()[2] not in tag_t_1:
                    tag_t_1[line.split()[2]] = 1
                else:
                    tag_t_1[line.split()[2]] += 1

    with open(test_file, "r") as f:
        for line in f.readlines():
            testData.append(line.split()[0])

    for i in range(len(filedata)):
        if i == 0:
            if filedata[i][1] not in trans_mat["initial"]:
                trans_mat['initial'][filedata[i][1]] = 1 / tag_t_1['initial']
            else:
                trans_mat['initial'][filedata[i][1]] += 1 / tag_t_1['initial']
        elif filedata[i - 1][0] in ['.', '!', '?', '"']:
            if filedata[i][1] not in trans_mat['initial']:
                trans_mat['initial'][filedata[i][1]] = 1 / tag_t_1['initial']
            else:
                trans_mat['initial'][filedata[i][1]] += 1 / tag_t_1['initial']
        else:
            if filedata[i - 1][1] not in trans_mat:
                trans_mat[filedata[i - 1][1]] = {}
            if filedata[i][1] not in trans_mat[filedata[i - 1][1]]:
                trans_mat[filedata[i - 1][1]][filedata[i][1]] = 1 / tag_t_1[filedata[i - 1][1]]
            else:
                trans_mat[filedata[i - 1][1]][filedata[i][1]] += 1 / tag_t_1[filedata[i - 1][1]]

        if filedata[i][1] not in emi_mat:
            emi_mat[filedata[i][1]] = {}
        if filedata[i][0] not in emi_mat[filedata[i][1]]:
            emi_mat[filedata[i][1]][filedata[i][0]] = 1 / tag_t[filedata[i][1]]
        else:
            emi_mat[filedata[i][1]][filedata[i][0]] += 1 / tag_t[filedata[i][1]]

    trans_mat = dict((k, dict((s, np.log(x)) for s, x in v.items())) for k, v in trans_mat.items())
    emi_mat = dict((k, dict((s, np.log(x)) for s, x in v.items())) for k, v in emi_mat.items())

    prob_trellis = {}
    result = ''
    for i in range(len(testData)):
        new_prob_trellis = {}
        if i == 0:
            for s in tag_t:
                trans_prob = trans_mat['initial'][s] if s in trans_mat['initial'] else -13
                emi_prob = emi_mat[s][testData[i]] if testData[i] in emi_mat[s] else -13
                new_prob_trellis[s] = trans_prob + emi_prob
        elif testData[i - 1][0] in ['.', '!', '?', '"']:
            for s in tag_t:
                trans_prob = trans_mat['initial'][s] if s in trans_mat['initial'] else -13
                emi_prob = emi_mat[s][testData[i]] if testData[i] in emi_mat[s] else -13
                new_prob_trellis[s] = trans_prob + emi_prob
            if testData[i - 1][0] == '"':
                result += (testData[i - 1] + ' : ' + 'PUQ' + '\n')
            else:
                result += (testData[i - 1] + ' : ' + 'PUN' + '\n')

        else:
            s_pre = {}
            for s in tag_t:
                new_prob_trellis[s] = float('-inf')
                for x in prob_trellis:
                    if x in trans_mat:
                        trans_prob = trans_mat[x][s] if s in trans_mat[x] else -13
                        emi_prob = emi_mat[s][testData[i]] if testData[i] in emi_mat[s] else -13
                        prob = prob_trellis[x] + trans_prob + emi_prob
                        if new_prob_trellis[s] < prob:
                            new_prob_trellis[s] = prob
                            s_pre[s] = x
            result += (testData[i - 1] + ' : ' + s_pre[max(new_prob_trellis, key=lambda key: new_prob_trellis[key])] + '\n')

        if i == len(testData) - 1:
            result += (testData[i] + ' : ' + max(new_prob_trellis, key=lambda key: new_prob_trellis[key]) + '\n')
        prob_trellis = new_prob_trellis
    with open(output_file, "w") as f:
        f.write(result)


if __name__ == '__main__':
    # Run the tagger function.
    print("Starting the tagging process.")

    # Tagger expects the input call: "python3 tagger.py -d <training files> -t <test file> -o <output file>"
    parameters = sys.argv
    training_list = parameters[parameters.index("-d")+1:parameters.index("-t")]
    test_file = parameters[parameters.index("-t")+1]
    output_file = parameters[parameters.index("-o")+1]
    print("Training files: " + str(training_list))
    # print("Test file: " + test_file)
    # print("Ouptut file: " + output_file)

    # Start the training and tagging operation.
    tag (training_list, test_file, output_file)
