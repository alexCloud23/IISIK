# ЛР4: примеры GraphQL-запросов для GraphiQL (http://127.0.0.1:8000/graphql)

## Фильтрация и сортировка (Query)

query { products { id name category currentPrice costPrice isActive } }

query { products(category: "Электроника") { id name currentPrice } }

query { products(search: "pro", orderBy: CURRENT_PRICE, orderDirection: DESC) { name currentPrice } }

query { products(minPrice: 500, maxPrice: 3000, orderBy: NAME) { name currentPrice } }

query { priceRecommendations(status: NEW, orderBy: RECOMMENDED_PRICE, orderDirection: ASC) { id status recommendedPrice rationale } }

query { notifications(isRead: false, notificationType: "FORECAST_READY") { id message notificationType isRead } }

query { product(id: "20000000-0000-4000-8000-000000000001") { id name currentPrice costPrice } }

query { demandForecasts { id productId forecastPeriod predictedDemand confidence } }

query { competitorStrategies { id productId strategyType competitorPrice description } }

query {
  priceRecommendations {
    id
    status
    currentPrice
    recommendedPrice
    rationale
    product { id name currentPrice }
  }
}

query { analyticsResults { id analysisType result } }

## Агрегации

query { salesSummary(productId: "20000000-0000-4000-8000-000000000001") { productId ordersCount totalQuantity avgUnitPrice } }

query { unreadNotificationsCount }

query { recommendationsSummary { total newCount acceptedCount rejectedCount } }

## Бизнес-операции (Mutation)

mutation {
  createProduct(input: { name: "Планшет Nova 10", category: "Электроника", price: 1899.99, description: "Планшет 11 дюймов" }) {
    id name currentPrice isActive
  }
}

mutation {
  updateProduct(id: "20000000-0000-4000-8000-000000000001", input: { price: 1259.00 }) {
    id name currentPrice
  }
}

mutation {
  updateProduct(id: "20000000-0000-4000-8000-000000000005", input: { isActive: true }) {
    id isActive
  }
}

# Генерация ценовой рекомендации: товар + последний прогноз + стратегия конкурента,
# расчёт цены и создание уведомления RECOMMENDATION_CREATED
mutation {
  generatePriceRecommendation(productId: "20000000-0000-4000-8000-000000000004") {
    id status recommendedPrice rationale
  }
}

# Принятие/отклонение рекомендации (только из статуса NEW), создаёт уведомление
mutation {
  decideRecommendation(id: "70000000-0000-4000-8000-000000000001", decision: ACCEPTED) {
    id status recommendedPrice
  }
}

mutation {
  markNotificationRead(id: "90000000-0000-4000-8000-000000000001") {
    id isRead
  }
}

mutation { markAllNotificationsRead }

## Коды ошибок (extensions.code)

- INVALID_ID — некорректный идентификатор (422)
- NOT_FOUND — объект не найден (404)
- INVALID_FILTER — некорректный параметр фильтрации/сортировки (422)
- INVALID_INPUT — некорректные значения полей (400)
- INVALID_OPERATION — нарушение бизнес-условия/состояния (409)
- UPSTREAM_UNAVAILABLE — сервис недоступен (502)
