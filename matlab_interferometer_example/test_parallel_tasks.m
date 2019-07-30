clear all
close all
clc

% parallel.defaultClusterProfile('local')
% cluster = parcluster()
% delete(cluster.Jobs)
% 
% job1 = createJob(cluster)

% pool = parpool(2);

pool = gcp();
queue = parallel.pool.PollableDataQueue;

future = parfeval(pool,@(num)testFun(num),1,1)
wait(future)

% spmd(1)
%     value = poll(queue)
%     if(~isempty(value))
%         randWait = rand()*4+1
%         pause(randWait)
%         disp('Value: ', value, ', Waiting secs: ', randWait)
%     end
% end

function ret = testFun(num)
    disp(num)
    while(1)
        value = []
    %     value = poll(queue)
        if(~isempty(value))
            randWait = rand()*4+1
            pause(randWait)
            disp('Value: ', value, ', Waiting secs: ', randWait)
        end
    end
end

