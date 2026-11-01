import encoding_demo_pb2 as ed

examples = {
    "a = 300": ed.Demo(a=300),
    "b = 'testing'": ed.Demo(b="testing"),
    "negative = -1 (int32)": ed.Demo(negative=-1),
    "zigzag = -1 (sint32)": ed.Demo(zigzag=-1),
    "zigzag = 1 (sint32)": ed.Demo(zigzag=1),
    "nums = [1, 2, 300]": ed.Demo(nums=[1, 2, 300]),
}
for title, message in examples.items():
    raw = message.SerializeToString()
    print(f"{title:<24} {len(raw):>2} байт: {raw.hex(' ')}")