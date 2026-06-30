from modules.embedding import get_embedding_model

model1 = get_embedding_model()
model2 = get_embedding_model()

print(model1 is model2)