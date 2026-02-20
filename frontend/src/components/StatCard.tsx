import clsx from 'clsx';
import { LucideIcon } from 'lucide-react';

interface StatCardProps {
    title: string;
    value: string | number;
    icon: LucideIcon;
    trend?: string;
    color?: 'blue' | 'green' | 'red' | 'purple';
}

export function StatCard({ title, value, icon: Icon, trend, color = 'blue' }: StatCardProps) {
    const colors = {
        blue: 'bg-blue-500/10 text-blue-500',
        green: 'bg-green-500/10 text-green-500',
        red: 'bg-red-500/10 text-red-500',
        purple: 'bg-purple-500/10 text-purple-500',
    };

    return (
        <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
            <div className="flex items-center justify-between mb-4">
                <h3 className="text-gray-400 text-sm font-medium">{title}</h3>
                <div className={clsx('p-2 rounded-lg', colors[color])}>
                    <Icon size={20} />
                </div>
            </div>
            <div className="flex items-baseline justify-between">
                <h2 className="text-3xl font-bold text-white">{value}</h2>
                {trend && <span className="text-green-400 text-sm">{trend}</span>}
            </div>
        </div>
    );
}
