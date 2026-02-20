import { useState, useEffect, useRef } from 'react';

const WS_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:8000/ws/dashboard';

export interface DashboardStats {
    total_sales: number;
    today_sales: number;
    order_count: number;
}

export function useWebSocket() {
    const [stats, setStats] = useState<DashboardStats | null>(null);
    const [isConnected, setIsConnected] = useState(false);
    const ws = useRef<WebSocket | null>(null);

    useEffect(() => {
        // Determine WS URL based on current location if env not set
        const url = WS_URL.startsWith('http')
            ? WS_URL.replace('http', 'ws')
            : WS_URL;

        function connect() {
            ws.current = new WebSocket(url);

            ws.current.onopen = () => {
                console.log('WS Connected');
                setIsConnected(true);
            };

            ws.current.onmessage = (event) => {
                try {
                    const data = JSON.parse(event.data);
                    setStats(data);
                } catch (e) {
                    console.error('Failed to parse WS msg', e);
                }
            };

            ws.current.onclose = () => {
                console.log('WS Disconnected');
                setIsConnected(false);
                // Reconnect
                setTimeout(connect, 3000);
            };
        }

        connect();

        return () => {
            ws.current?.close();
        };
    }, []);

    return { stats, isConnected };
}
