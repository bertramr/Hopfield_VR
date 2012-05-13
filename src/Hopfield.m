classdef Hopfield
    properties
        N
        P
        pattern
        weight

        x

        meanRetrievalError
        tmax
    end
    
    properties (Dependent=true)
        overlap
        energy
        pixelDistance
    end
    
    methods
        function obj = Hopfield(N)
            obj.N = N;
            obj.tmax = 20;
        end
        
        function obj = create_pattern(obj, P, ratio)
            obj.P = P;
            idx = ceil(ratio * obj.N);
            obj.pattern = [-ones(P,idx) ones(P,obj.N-idx)];
            
            
            for i = 1:P
                perm = randperm(obj.N);
                obj.pattern(i,:) = obj.pattern(i,perm);
            end
            
        end
        
        function obj = calc_weight(obj)
            obj.weight = zeros(obj.N);
            
            for p = 1:obj.P
                obj.weight = obj.weight + 1/obj.N * obj.pattern(p,:)' * obj.pattern(p,:);
            end
            obj.weight(logical(eye(obj.N))) = 0;
        end
        
        function obj = set_init_state(obj,mu,flip_ratio)
            obj.x = obj.pattern(mu,:);
            
            idx = ceil(flip_ratio * obj.N);
            flip = [-ones(1,idx) ones(1,obj.N-idx)];
            
            flip = flip(randperm(obj.N));
            
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
            % Alte Formulierung im Intervall [-1 1]
            overlap =   sum(obj.pattern .* repmat(obj.x,obj.P,1),2) / obj.N;
        end
        
        function dist = get.pixelDistance(obj)
            %% Exersice 1.2
            % Umwandlung (overlap + 1)*1/2
            % Im Intervall [0 1] entspricht Prozent
            dist =  sum(obj.pattern == repmat(obj.x,obj.P,1),2) / obj.N;
            
        end
        function energy = get.energy(obj)
            energy = - sum(sum(obj.weight .* (obj.x' * obj.x)));
        end
        
        function obj = run(obj, P, ratio, mu, flip_ratio, bPlot)
            obj = obj.create_pattern(P, ratio);
            obj = obj.calc_weight;
            obj = obj.set_init_state(mu,flip_ratio);
            
            time = cumsum(ones(obj.tmax * obj.N,1))/obj.N;
            energy = zeros(obj.tmax * obj.N,1);
            overlap = zeros(obj.tmax * obj.N,1);
            
            c = 1;
            for t = 1:obj.tmax
                x_old = obj.x;
                for n = randperm(obj.N)
                    obj = obj.dynamic(n);
                    energy(c) = obj.energy;
                    overlap(c) = obj.overlap(mu);
                    c = c+1;
                end
                if x_old == obj.x;
                    energy = energy(1:c-1);
                    overlap = overlap(1:c-1);
                    time = time(1:c-1);
                    break;
                end
            end
            if bPlot
                figure;
                subplot(2,1,1);
                plot(time,energy);
                subplot(2,1,2);
                plot(time,overlap);
            end
            obj.meanRetrievalError = obj.pixelDistance;
        end
    end
    
end