# @Time: 03/31/2021
# @Author: Litong Peng
# @Email: lp5629@rit.edu

from math import log


# transfer the decimal address to binary address
# :param split: 4-split decimal address list
# :return: 32 bits address string
def to_binary(split):
    binary = ''
    for s in split:
        s_binary = bin(int(s))
        s_binary_len = len(str(s_binary)[2:])
        binary += ('0' * (8 - s_binary_len) + str(bin(int(s)))[2:])
    return binary


# calculate the zero number in a binary address
# :param binary: the 32 bits binary address string
# :return: how many zero in this address
def zero_num(binary):
    one = True
    zero = 0
    for ib in binary:
        if ib == '1' and one:
            continue
        elif ib == '0' and one:
            one = False
        elif ib == '0' and not one:
            zero += 1
    return zero


# transfer the binary address to decimal adress
# :param binary: binary address string
# :return: decimal address string
def to_decimal(binary):
    deci = ''
    deci += str(int(binary[:8], 2)) + '.'
    deci += str(int(binary[8:16], 2)) + '.'
    deci += str(int(binary[16:24], 2)) + '.'
    deci += str(int(binary[24:32], 2))
    return deci


# add the dots in binary address
# :param binary: binary address string without dots
# :return: binary address string with dots
def binary_dot(binary):
    i = 0
    dots = ''
    while i < len(binary):
        dots += binary[i:i + 8] + '.'
        i += 8
    return dots


# complete the 'subnet_bit'-length bits using 0
# :param num: the number I want to fill 0
# :param subnet_bit: complete to how long
# :return: 'subnet_bit'-length bits num
def fill(num, subnet_bit):
    return '0' * (subnet_bit - len(num)) + num


# the main program
def main():
    # Checking for a valid IP Address
    while True:
        ip = input("Please enter IP address: ")
        ip_split = ip.split('.')
        ip_binary = to_binary(ip_split)
        if (len(ip_split) == 4) and (0 <= int(ip_split[0]) <= 255) and \
                (ip_binary[0] == '0' or ip_binary[:2] == '10' or ip_binary[:3] == '110') and \
                (0 <= int(ip_split[1]) <= 255) and (0 <= int(ip_split[2]) <= 255) and (0 <= int(ip_split[3]) <= 255):
            break
        else:
            print('The ip address is invalid, please re-enter!')
            print('Here is an ip address example format: 192.168.1.0')
            continue

    # find the subnet mask address
    # Class A
    if ip_binary[0] == '0':
        mask = '255.0.0.0'
    # Class B
    elif ip_binary[:2] == '10':
        mask = '255.255.0.0'
    # Class C
    elif ip_binary[:3] == '110':
        mask = '255.255.255.0'
    mask_split = mask.split('.')
    mask_binary = to_binary(mask_split)
    mask_zero = zero_num(mask_binary)
    subnets = [str(2 ** n) for n in range(mask_zero + 1)]

    # checking for a valid subnet number
    while True:
        subnet_num = input('Please enter desired subnet number: ')
        if subnet_num not in subnets:
            print('The subnet number is invalid, please re-enter!')
            print('Here is an subnet number example format: 16')
            continue
        else:
            break
    # Required output

    # •	The current network, mask, range of addresses and a possible high and low router address.
    network = int(ip_binary, 2) & int(mask_binary, 2)
    print('\n----------------------------------------------------')
    print("The current network is: \n" + 'decimal: ' + to_decimal(str(bin(network))[2:]) + ',\nbinary: ' + binary_dot(
        str(bin(network))[2:]))
    print('\nThe current mask is: ' + mask)
    low = str(bin(network))[2:][:(32 - mask_zero)] + '0' * mask_zero
    high = str(bin(network))[2:][:(32 - mask_zero)] + '1' * mask_zero
    print('\nThe range of the address is: ' + to_decimal(low) + ' to ' + to_decimal(high))
    print('\nThe possible high address is: ' + binary_dot(high[:31] + '0'))
    print('\nThe possible low address is: ' + binary_dot(low[:31] + '1'))

    # •	The number of bits needed to be stolen
    subnet_bit = int(log(int(subnet_num), 2))
    print('\n----------------------------------------------------')
    print('The number of bits needed to be stolen is: ' + str(subnet_bit))

    # •	The new subnet mask in binary and base 10 numbers.
    new_mask = (32 - mask_zero + subnet_bit) * '1' + (mask_zero - subnet_bit) * '0'
    print('\n----------------------------------------------------')
    print('The new subnet mask is: \n' + 'decimal: ' + to_decimal(new_mask) + ',\nbinary: ' + binary_dot(new_mask))

    # •	The number of subnets created
    print('\n----------------------------------------------------')
    print('The number of subnets created is: ' + subnet_num)

    # •	The total number of hosts per subnet
    print('\n----------------------------------------------------')
    print('The total number of hosts per subnet is: ' + str(2 ** mask_zero))

    # •	The subnet range for the first 5 subnets or the number of requested subnets,
    # whichever is higher – in binary and base 10 numbers
    if subnet_bit >= 3:
        subnets5_begin = ip_binary[:32 - mask_zero] + '0' * (subnet_bit - 3) + '000' + '0' * (mask_zero - subnet_bit)
        subnets5_end = ip_binary[:32 - mask_zero] + '0' * (subnet_bit - 3) + '100' + '0' * (mask_zero - subnet_bit)
        print('\n----------------------------------------------------')
        print('The subnets are more than 5, the first 5 subnets are:\n'
              'decimal: ' + to_decimal(subnets5_begin) + ' to ' + to_decimal(subnets5_end) + '\n'
              'binary: ' + binary_dot(subnets5_begin) + ' to ' + binary_dot(subnets5_end))
    else:
        if subnet_bit == 1:
            subnets1_begin = ip_binary[:32 - mask_zero] + '0' * mask_zero
            subnets1_end = ip_binary[:32 - mask_zero] + '0' * (subnet_bit - 1) + '1' + '0' * (mask_zero - subnet_bit)
            print('\n----------------------------------------------------')
            print('The subnets are less than 5, which are:\n'
                  'decimal: ' + to_decimal(subnets1_begin) + ' to ' + to_decimal(subnets1_end) + '\n'
                  'binary: ' + binary_dot(subnets1_begin) + ' to ' + binary_dot(subnets1_end))
        elif subnet_bit == 2:
            subnets2_begin = ip_binary[:32 - mask_zero] + '0' * (subnet_bit - 2) + '00' + '0' * (mask_zero - subnet_bit)
            subnets2_end = ip_binary[:32 - mask_zero] + '0' * (subnet_bit - 2) + '11' + '0' * (mask_zero - subnet_bit)
            print('\n----------------------------------------------------')
            print('The subnets are less than 5, which are:\n'
                  'decimal: ' + to_decimal(subnets2_begin) + ' to ' + to_decimal(subnets2_end) + '\n'
                  'binary: ' + binary_dot(subnets2_begin) + ' to ' + binary_dot(subnets2_end))

    # •	The subnet range for the last subnet – in binary and base 10 numbers
    last_begin = ip_binary[:32 - mask_zero + subnet_bit] + '0' * (mask_zero - subnet_bit)
    last_end = ip_binary[:32 - mask_zero + subnet_bit] + '1' * (mask_zero - subnet_bit)
    print('\n----------------------------------------------------')
    print('The subnet range for the last subnet is:\n'
          + 'decimal: ' + to_decimal(last_begin) + ' to ' + to_decimal(last_end) + '\n'
          + 'binary: ' + binary_dot(last_begin) + ' to ' + binary_dot(last_end))

    # •	The range of usable addresses in each
    first = 0
    subnet_fill = []
    while first < int(subnet_num):
        subnet_fill.append(fill(bin(first)[2:], subnet_bit))
        first += 1
    print('\n----------------------------------------------------')
    print('The range of usable addresses are:')
    for s in subnet_fill:
        usable_begin = ip_binary[:32 - mask_zero] + s + (mask_zero - subnet_bit - 1) * '0' + '1'
        usable_end = ip_binary[:32 - mask_zero] + s + (mask_zero - subnet_bit - 1) * '1' + '0'
        print('decimal: ' + to_decimal(usable_begin) + ' to ' + to_decimal(usable_end) + '\n'
              + 'binary: ' + binary_dot(usable_begin) + ' to ' + binary_dot(usable_end))

    # •	Possible low and high router addresses for each subnet
    print('\n----------------------------------------------------')
    print('Possible low and high router addresses for each subnet are:')
    for s in subnet_fill:
        low = ip_binary[:32 - mask_zero] + s + (mask_zero - subnet_bit - 1) * '0' + '1'
        high = ip_binary[:32 - mask_zero] + s + (mask_zero - subnet_bit - 1) * '1' + '0'
        print('decimal: low:' + to_decimal(low) + ', high: ' + to_decimal(high) + '\n'
              + 'binary: low:' + binary_dot(low) + ',high: ' + binary_dot(high))

    # •	Identify the network IDs and the broadcast addresses
    print('\n----------------------------------------------------')
    print("the network IDs and the broadcast addresses are:")
    for s in subnet_fill:
        print('\nthe network IDs are:')
        net_id = ip_binary[:32 - mask_zero] + s + (mask_zero - subnet_bit) * '0'
        print('decimal:' + to_decimal(net_id) + '\nbinary: ' + binary_dot(net_id))
        print('the broadcast addresses are:')
        broadcast = ip_binary[:32 - mask_zero] + s + (mask_zero - subnet_bit) * '1'
        print('decimal:' + to_decimal(broadcast) + '\nbinary: ' + binary_dot(broadcast))


if __name__ == '__main__':
    main()
