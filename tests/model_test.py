from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# Імітація результатів класифікації
true_labels = [1, 1, 0, 0, 1, 0, 1]  # 1 - фейк, 0 - реальне
predicted_labels = [1, 0, 0, 0, 1, 0, 1]  # Передбачення моделі

# Розрахунок метрик
accuracy = accuracy_score(true_labels, predicted_labels)
precision = precision_score(true_labels, predicted_labels)
recall = recall_score(true_labels, predicted_labels)
f1 = f1_score(true_labels, predicted_labels)

print("[INFO] Metrics for model evaluation:")
print(f"Accuracy: {accuracy * 100:.2f}%")
print(f"Precision: {precision * 100:.2f}%")
print(f"Recall: {recall * 100:.2f}%")
print(f"F1-Score: {f1 * 100:.2f}%")
