import { Activity, DollarSign, Package, ShoppingCart } from 'lucide-react';
import { useWebSocket } from '../hooks/useWebSocket';
import { StatCard } from './StatCard';

export function Dashboard() {
    const { stats, isConnected } = useWebSocket();

    if (!isConnected && !stats) {
        return (
            <div className="flex items-center justify-center h-64">
                <div className="text-gray-400 animate-pulse">Connecting to Live Stream...</div>
            </div>
        );
    }

    const sales = stats?.total_sales || 0;
    const today = stats?.today_sales || 0;
    const orders = stats?.order_count || 0;

    return (
        <div className="p-8 max-w-7xl mx-auto">
            <div className="flex items-center justify-between mb-8">
                <div>
                    <h1 className="text-3xl font-bold text-white mb-2">Operations Dashboard</h1>
                    <p className="text-gray-400">StreamStock Real-Time Overview</p>
                </div>
                <div className="flex items-center space-x-2">
                    <span className={`w-3 h-3 rounded-full ${isConnected ? 'bg-green-500' : 'bg-red-500'}`}></span>
                    <span className="text-sm text-gray-400">{isConnected ? 'Live' : 'Disconnected'}</span>
                </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
                <StatCard
                    title="Total Revenue"
                    value={`$${sales.toLocaleString()}`}
                    icon={DollarSign}
                    color="green"
                />
                <StatCard
                    title="Today's Sales"
                    value={`$${today.toLocaleString()}`}
                    icon={Activity}
                    color="blue"
                />
                <StatCard
                    title="Total Orders"
                    value={orders.toLocaleString()}
                    icon={ShoppingCart}
                    color="purple"
                />
                <StatCard
                    title="Active Inventory"
                    value="1,240"
                    icon={Package}
                    color="red"
                // Mock value for now until we add inventory aggregate
                />
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                <div className="lg:col-span-2 bg-gray-800 rounded-xl border border-gray-700 p-6 min-h-[400px]">
                    <h3 className="text-lg font-semibold text-white mb-4">Live Inventory</h3>
                    {/* InventoryTable placeholder */}
                    <div className="text-gray-500 text-center py-20">No data available</div>
                </div>
                <div className="bg-gray-800 rounded-xl border border-gray-700 p-6">
                    <h3 className="text-lg font-semibold text-white mb-4">Recent Alerts</h3>
                    {/* AlertsFeed placeholder */}
                    <div className="space-y-4">
                        <div className="p-3 bg-red-500/10 border border-red-500/20 rounded-lg">
                            <p className="text-red-400 text-sm font-medium">Low Stock: SKU-123</p>
                            <p className="text-gray-500 text-xs mt-1">2 mins ago</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
