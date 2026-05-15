import re

def fix_subtitles(original_en, translated_it, output_file):
    timestamp_pattern = re.compile(r'(\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3})')
    
    with open(original_en, 'r', encoding='utf-8') as f:
        en_content = f.read()
    
    en_timestamps = timestamp_pattern.findall(en_content)

    with open(translated_it, 'r', encoding='utf-8') as f:
        it_content = f.read()

    it_blocks = re.split(r'\n\s*\n', it_content.strip())
    
    fixed_blocks = []
    
    for i, block in enumerate(it_blocks):
        lines = block.strip().split('\n')
        
        text_start_index = 0
        for idx, line in enumerate(lines):
            if '-->' in line:
                text_start_index = idx + 1
                break
        
        subtitle_text = lines[text_start_index:]
        
        new_index = str(i + 1)
        
        if i < len(en_timestamps):
            new_timestamp = en_timestamps[i]
        else:
            ts_match = timestamp_pattern.search(block)
            new_timestamp = ts_match.group(0) if ts_match else "00:00:00,000 --> 00:00:00,000"

        new_block = [new_index, new_timestamp] + subtitle_text
        fixed_blocks.append('\n'.join(new_block))

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(fixed_blocks))
    
    print(f"Completato! {len(fixed_blocks)} entry processate.")
    print(f"File salvato in: {output_file}")

fix_subtitles('finding_satoshi_sub_eng.srt', 'finding_satoshi_sub_ita.srt', 'finding_satoshi_sub_ita_fixed.srt')
