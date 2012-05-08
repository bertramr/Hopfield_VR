classdef Hopfield
    properties
        N
        P
        pattern
        weight
        x
        
        tmax
    end
    
    properties (Dependent=true)
        overlap
        energy
    end
    
    methods
        function obj = Hopfield(N)
            obj.N = N;
            obj.tmax = 20;
        end
        
        function obj = create_pattern(obj, P, ratio)
            obj.P = P;
            idx = ceil(ratio * obj.N);
            obj.pattern = -ones(P,obj.N);
            obj.pattern(:,1:idx) = 1;
            perm = zeros(P,obj.N);
            for i = 1:P
                perm(i,:) = randperm(obj.N);
            end
            obj.pattern(perm) = obj.pattern;
        end
        
        function obj = calc_weight(obj)
            obj.weight = zeros(obj.N);
            
            for i = 1:obj.N
                for j = 1:obj.N
                    if i ~= j
                        obj.weight(i,j) = 1/obj.N * ...
                            sum(obj.pattern(:,i) .* obj.pattern(:,j));
                    end
                end
            end
            
        end
        
        function obj = set_init_state(obj,mu,flip_ratio)
            obj.x = obj.pattern(mu,:);
            
            flip = rand(1,obj.N) <= flip_ratio;
            
            flip = -ones(1,obj.N) .* flip + ones(1,obj.N) .* ~flip;
            
            obj.x = obj.x .* flip;
        end
        
        
        function obj = dynamic(obj,j)
            var = obj.x * obj.weight;
            if var(j) == 0
                obj.x(j) = 1;
            else
                obj.x(j) = sign(var(j));
            end
        end
        
        function overlap = get.overlap(obj)
            
            overlap =   obj.pattern .* repmat(obj.x,obj.P,1) / obj.N;
        end
        
        function energy = get.energy(obj)
            e = 0;
            for i = 1:obj.N
                for j = 1:obj.N
                    e = e + obj.weight(i,j) * obj.x(i) * obj.x(j);
                end
            end
            energy = -e;
        end
        
        function obj = run(obj, P, ratio, mu, flip_ratio)
            obj = obj.create_pattern(P, ratio);
            obj = obj.calc_weight;
            obj = obj.set_init_state(mu,flip_ratio);
            
            time = cumsum(ones(obj.tmax * obj.N,1))/obj.N;
            energy = zeros(obj.tmax * obj.N,1);
            overlap = zeros(obj.tmax * obj.N,1);
            
            c = 1;
            for t = 1:obj.tmax
                for n = 1:obj.N
                    obj = obj.dynamic(n);
                    energy(c) = obj.energy;
                    overlap(c) = obj.overlap(mu);
                    c = c+1;
                end
            end
            
            figure;
            subplot(2,1,1);
            plot(time,energy);
            subplot(2,1,2);
            plot(time,overlap);
            
        end
    end
    
end