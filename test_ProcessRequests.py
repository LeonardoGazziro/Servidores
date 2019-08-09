def test_ProcessRequests():
    import Servers_2

    inputs = ['input1.txt', 'input2.txt']
    outputs = ['output1.txt', 'output2.txt']

    for idx in range(len(inputs)):
        sp = Servers_2.ServerRequests()
        sp.process_requests(inputs[idx])

        process_output = open(outputs[idx], 'r')
        correct_output = open('output.txt', 'r')

        for line in process_output:
             assert line.strip() == correct_output.readline().strip()

        process_output.close()
        correct_output.close()
