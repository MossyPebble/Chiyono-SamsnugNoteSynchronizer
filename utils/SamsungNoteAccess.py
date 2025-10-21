from pathlib import Path

def find_all(hay, needle):
    i=0; out=[]
    while True:
        j = hay.find(needle, i)
        if j<0: break
        out.append(j); i = j+1
    return out

def extract_from_dotnote(file_path):
    
    # 해당 파일에는 반드시 __START__ 와 __END__ 가 존재해야 함
    start_marker = "START".encode("utf-16-le")
    end_marker = "END".encode("utf-16-le")
    if not start_marker or not end_marker:
        raise ValueError("Start or end marker cannot be empty.")

    data = Path(file_path).read_bytes()
    start_indices = find_all(data, start_marker)
    end_indices = find_all(data, end_marker)
    extracted_segments = ""

    for start in start_indices:

        # Find the nearest end marker after the start marker
        end = next((e for e in end_indices if e > start), None)
        if end:
            segment = data[start + len(start_marker):end]
            try:
                decoded_segment = segment.decode("utf-16-le").strip()
                if decoded_segment:
                    extracted_segments += decoded_segment
            except UnicodeDecodeError:
                continue

    return extracted_segments

if __name__ == "__main__":
    path = r"C:\Users\LG\AppData\Local\Packages\SAMSUNGELECTRONICSCoLtd.SamsungNotes_wyx1vj98g3asy\LocalState\wdoc\46976171-1965-ebf8-0000-017f178d5877\note.note"
    extracted_texts = extract_from_dotnote(path)
    print(extracted_texts)