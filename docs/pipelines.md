# Business Pipelines

## 1. Product Creation Flow

1.  **API**: `POST /products` -> Creates DB Record (Pending) -> Emits `product.created`.
2.  **InventoryProcessor**: Consumes `product.created` -> Initializes `InventoryItem` with 0 quantity.

## 2. Stock Restock Flow

1.  **External System / Script**: Emits `stock.received`.
2.  **InventoryProcessor**: Consumes `stock.received` -> Updates `InventoryItem` (+quantity).
3.  **AnalyticsProcessor**: Consumes `stock.received` -> Updates stock heatmaps.

## 3. Order Fulfillment Flow

This is the most complex saga.

1.  **API**: `POST /orders` -> Emits `order.created`.
2.  **OrderProcessor**: Consumes `order.created` -> Creates `Order` (PENDING).
3.  **InventoryProcessor**: Consumes `order.created`.
    -   Checks stock.
    -   **If Sufficient**: Reserves stock -> Emits `stock.reserved`.
    -   **If Insufficient**: Emits `order.cancelled` (Reason: OOS).
4.  **OrderProcessor**:
    -   Consumes `stock.reserved` -> Checks if all items reserved (logic simplified in demo).
    -   Consumes `order.cancelled` -> Updates Order Status to CANCELLED.
    -   (Future) Emits `order.confirmed` if reservations complete.
5.  **AnalyticsProcessor**: Consumes `order.created` -> Increments Sales Counter.

## 4. Low Stock Alerting

1.  **InventoryProcessor**: Detects low stock during update -> Emits `stock.low`.
2.  **RestockProcessor**: Consumes `stock.low` -> Generates Draft PO.
3.  **AlertProcessor**: Consumes `stock.low` -> Pushes to WebSocket & Audit Log.
