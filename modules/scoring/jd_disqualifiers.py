import re
from typing import Dict

def has_only_consulting_experience(candidate) -> bool:
    """
    Check if the candidate has only worked at consulting/IT services firms.
    """
    consulting_companies = {
        'infosys', 'wipro', 'tcs', 'capgemini', 'hcl', 
        'mindtree', 'accenture', 'cognizant', 'tech mahindra', 'mphasis'
    }
    
    if not candidate.career_history:
        return False
        
    return all(
        job.company.lower() in consulting_companies or job.industry.lower() in {'it services', 'consulting'}
        for job in candidate.career_history
    )

def is_pure_research_no_prod(candidate) -> bool:
    """
    Check if candidate's roles are academic/research-oriented with zero production/deployment evidence.
    """
    research_titles = {'research', 'academic', 'scientist', 'postdoc', 'phd'}
    has_research_role = any(
        any(word in job.title.lower() for word in research_titles)
        for job in candidate.career_history
    )
    if not has_research_role:
        return False
        
    prod_keywords = {
        'deploy', 'production', 'productionize', 'ship', 'serve', 
        'scale', 'user', 'customer', 'k8s', 'kubernetes', 'docker', 
        'terraform', 'aws', 'gcp', 'azure', 'api', 'system', 'product', 'cloud'
    }
    
    all_descriptions = " ".join(
        job.description.lower() for job in candidate.career_history
    )
    
    has_prod_mention = any(word in all_descriptions for word in prod_keywords)
    return not has_prod_mention

def is_recent_langchain_only(candidate) -> bool:
    """
    Check if candidate's AI experience is purely recent LLM/LangChain calling
    without any traditional ML/NLP background.
    """
    llm_skills = {'langchain', 'openai', 'gpt', 'llm', 'prompt engineering'}
    traditional_ml_skills = {
        'machine learning', 'scikit-learn', 'tensorflow', 'pytorch', 'nlp', 
        'natural language processing', 'search', 'retrieval', 'indexing', 
        'faiss', 'bm25', 'milvus', 'chromadb', 'qdrant', 'pinecone', 'solr', 
        'elasticsearch', 'opensearch', 'xgboost', 'pandas', 'numpy', 'scipy',
        'statsmodels', 'regression', 'classification', 'clustering'
    }
    
    candidate_skills = {s.name.lower() for s in candidate.skills}
    has_llm = any(s in candidate_skills for s in llm_skills)
    has_traditional = any(s in candidate_skills for s in traditional_ml_skills)
    
    return has_llm and not has_traditional

def is_inactive_senior_architect(candidate) -> bool:
    """
    Check if the candidate is a Senior/Lead/Architect who hasn't coded in the last 18 months.
    """
    lead_titles = {'architect', 'tech lead', 'technical lead', 'engineering manager', 'director'}
    if not candidate.career_history:
        return False
        
    current_job = candidate.career_history[0]
    if not current_job.is_current:
        return False
        
    is_lead = any(word in current_job.title.lower() for word in lead_titles)
    if not is_lead:
        return False
        
    if current_job.duration_months < 18:
        return False
        
    coding_keywords = {'code', 'write', 'develop', 'program', 'python', 'implement', 'build', 'c++', 'rust', 'go', 'java'}
    desc = current_job.description.lower()
    has_coding = any(word in desc for word in coding_keywords)
    
    return not has_coding

def is_cv_speech_only_no_nlp(candidate) -> bool:
    """
    Check if the candidate has only Computer Vision / Speech / Robotics experience with no NLP/IR.
    """
    cv_speech_skills = {
        'computer vision', 'speech', 'robotics', 'voice', 'audio', 'image', 
        'object detection', 'segmentation', 'tts', 'asr', 'speech recognition',
        'image classification', 'cnn', 'yolo', 'opencv'
    }
    nlp_ir_skills = {
        'nlp', 'natural language', 'retrieval', 'search', 'indexing', 'text', 
        'language model', 'llm', 'transformer', 'bert', 'gpt', 'rag', 'langchain',
        'bm25', 'vector database', 'semantic search', 'information retrieval'
    }
    
    candidate_skills = {s.name.lower() for s in candidate.skills}
    has_cv_speech = any(s in candidate_skills for s in cv_speech_skills)
    has_nlp_ir = any(s in candidate_skills for s in nlp_ir_skills)
    
    return has_cv_speech and not has_nlp_ir

def is_title_chaser(candidate) -> bool:
    """
    Check if the candidate hops companies very frequently (e.g. < 1.5 years on average)
    while fast-tracking title progression.
    """
    if len(candidate.career_history) < 3:
        return False
        
    durations = [job.duration_months for job in candidate.career_history]
    avg_duration = sum(durations) / len(durations)
    if avg_duration > 18:
        return False
        
    progression_titles = {'senior', 'staff', 'principal', 'lead', 'head'}
    has_progression = any(
        any(word in job.title.lower() for word in progression_titles)
        for job in candidate.career_history
    )
    return has_progression

def compute_disqualifier_penalty(candidate) -> float:
    """
    Calculate a combined multiplier based on matches with explicit disqualifiers.
    Returns a value in [0.0, 1.0], where 1.0 means no disqualification/penalty.
    """
    multiplier = 1.0
    
    if has_only_consulting_experience(candidate):
        multiplier *= 0.30
        
    if is_pure_research_no_prod(candidate):
        multiplier *= 0.40
        
    if is_recent_langchain_only(candidate):
        multiplier *= 0.50
        
    if is_inactive_senior_architect(candidate):
        multiplier *= 0.50
        
    if is_cv_speech_only_no_nlp(candidate):
        multiplier *= 0.50
        
    if is_title_chaser(candidate):
        multiplier *= 0.50
        
    return multiplier
