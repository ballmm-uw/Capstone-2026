import os
import glob
from collections import defaultdict, Counter

# Define paths
processed_folder = r"/Users/rowantabor/Desktop/capstone/data/transcript_entities"  # ← updated path
related_folder = r"/Users/rowantabor/Desktop/capstone/data/related_entities"

# Create output folder if it doesn't exist
os.makedirs(related_folder, exist_ok=True)

print("Analyzing entity files for related interviews...")

interview_entities = {}
interview_subjects = {}

files = glob.glob(os.path.join(processed_folder, "*_entities.txt"))
files = [f for f in files if not os.path.basename(f).startswith("_SUMMARY")]

if not files:
    print("No entity files found! Make sure you've run the entity extraction first.")
    exit()

print(f"Found {len(files)} interview entity files.")

for filepath in files:
    filename = os.path.splitext(os.path.basename(filepath))[0]
    interview_name = filename.replace("_entities", "")
    
    entities = {}
    interview_subject = "Unknown"
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
            if lines and lines[0].startswith("Interview Subject:"):
                interview_subject = lines[0].replace("Interview Subject:", "").strip()
            
            for line in lines:
                if any(x in line for x in ["Interview Subject:", "Source:", "Total entities:", 
                                           "ENTITY", "====", "----", "CONTEXT EXAMPLES"]):
                    continue
                
                if line and not line[0].isspace():
                    parts = line.split()
                    
                    if len(parts) >= 3:
                        count_index = None
                        for i, part in enumerate(parts):
                            try:
                                count = int(part)
                                count_index = i
                                break
                            except ValueError:
                                continue
                        
                        if count_index is not None and count_index >= 2:
                            entity_label = parts[count_index - 1]
                            entity_text = " ".join(parts[:count_index - 1])
                            entity_count = int(parts[count_index])
                            
                            if entity_text and entity_label:
                                entities[(entity_text, entity_label)] = entity_count
        
        interview_entities[interview_name] = entities
        interview_subjects[interview_name] = interview_subject
        
    except Exception as e:
        print(f"✗ Error reading {filepath}: {e}")

print(f"\nLoaded entities summary:")
for interview_name, entities in list(interview_entities.items())[:3]:
    print(f"  {interview_name}: {len(entities)} entities")
    if entities:
        for ent, count in list(entities.items())[:3]:
            print(f"    - {ent}: {count}")

print(f"\nTotal interviews: {len(interview_entities)}")
print(f"Total entities: {sum(len(ents) for ents in interview_entities.values())}")

if not any(interview_entities.values()):
    print("\nERROR: No entities were loaded!")
    exit()

print(f"\nGenerating related interview files...")

for source_interview, source_entities in interview_entities.items():
    related_interviews = []
    
    for target_interview, target_entities in interview_entities.items():
        if source_interview == target_interview:
            continue
        
        shared_entities = set(source_entities.keys()) & set(target_entities.keys())
        
        if shared_entities:
            total_shared_mentions = sum(source_entities[ent] + target_entities[ent] 
                                       for ent in shared_entities)
            
            related_interviews.append({
                'interview': target_interview,
                'subject': interview_subjects[target_interview],
                'shared_count': len(shared_entities),
                'total_mentions': total_shared_mentions,
                'shared_entities': shared_entities
            })
    
    related_interviews.sort(key=lambda x: (x['shared_count'], x['total_mentions']), reverse=True)
    
    output_file = os.path.join(related_folder, f"{source_interview}_related.txt")
    
    with open(output_file, 'w', encoding='utf-8') as out_file:
        out_file.write(f"RELATED INTERVIEWS FOR: {source_interview}\n")
        out_file.write(f"Interview Subject: {interview_subjects[source_interview]}\n")
        out_file.write(f"Total entities in this interview: {len(source_entities)}\n")
        out_file.write("=" * 120 + "\n\n")
        
        if not related_interviews:
            out_file.write("No related interviews found (no shared entities).\n")
        else:
            out_file.write(f"Found {len(related_interviews)} related interviews:\n\n")
            
            for i, related in enumerate(related_interviews, 1):
                out_file.write(f"{i}. {related['interview']}\n")
                out_file.write(f"   Subject: {related['subject']}\n")
                out_file.write(f"   Shared entities: {related['shared_count']}\n")
                out_file.write(f"   Total mentions: {related['total_mentions']}\n\n")
                out_file.write(f"   Shared entities:\n")
                
                for entity_text, entity_label in sorted(related['shared_entities'], 
                                                       key=lambda x: source_entities[x], 
                                                       reverse=True):
                    source_count = source_entities[(entity_text, entity_label)]
                    target_count = interview_entities[related['interview']][(entity_text, entity_label)]
                    out_file.write(f"     - {entity_text} ({entity_label}): "
                                 f"{source_count} mentions here, {target_count} mentions there\n")
                
                out_file.write("\n" + "-" * 120 + "\n\n")

print(f"\n{'='*50}")
print(f"Related interview analysis complete!")
print(f"Files saved in {related_folder}")
